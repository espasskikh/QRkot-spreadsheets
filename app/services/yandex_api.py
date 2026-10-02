import io
import re
from datetime import datetime, timedelta

import xlsxwriter
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.yandex_client import YandexDiskClient
from app.repositories.charity_project import charity_project_repository


SECONDS_IN_HOUR = 3600
SECONDS_IN_MINUTE = 60
INVALID_CHARS = re.compile(r'[\\/:*?"<>|]')


def format_time_delta(delta: timedelta) -> str:
    """Вернуть длительность в виде 'X дн. Y ч.' или 'Y ч. Z мин.'."""
    hours, remainder = divmod(delta.seconds, SECONDS_IN_HOUR)
    minutes = remainder // SECONDS_IN_MINUTE
    if delta.days:
        return f'{delta.days} дн. {hours} ч.'
    return f'{hours} ч. {minutes} мин.'


async def create_simple_report(
    projects: list,
    yandex_client: YandexDiskClient
) -> str:
    """Создать отчёт по проектам и вернуть публичную ссылку."""
    report_time = datetime.now().strftime(settings.report_format)
    filename = INVALID_CHARS.sub('', f'Отчет_{report_time}')

    upload_url, file_path = await yandex_client.create_excel_file(filename)

    with io.BytesIO() as output:
        with xlsxwriter.Workbook(output) as workbook:
            worksheet = workbook.add_worksheet('Отчёт')

            title_format = workbook.add_format({'bold': True, 'border': 1})
            header_format = workbook.add_format({
                'bold': True,
                'bg_color': '#2379C9',
                'font_color': 'white',
                'border': 1
            })
            cell_format = workbook.add_format({'border': 1})

            worksheet.merge_range(
                'A1:C1', f'Отчёт от {report_time}', title_format
            )
            for column, heading in enumerate(
                ('Название проекта', 'Время сбора', 'Описание')
            ):
                worksheet.write(1, column, heading, header_format)

            for row, project in enumerate(projects, start=2):
                duration = project['close_date'] - project['create_date']
                worksheet.write(row, 0, project['name'], cell_format)
                worksheet.write(
                    row, 1, format_time_delta(duration), cell_format
                )
                worksheet.write(row, 2, project['description'], cell_format)

            total_row = len(projects) + 2
            worksheet.write(total_row, 0, 'Всего проектов:', title_format)
            worksheet.write(total_row, 1, len(projects), title_format)
            worksheet.write_blank(total_row, 2, None, cell_format)

            worksheet.set_column('A:A', 40)
            worksheet.set_column('B:B', 20)
            worksheet.set_column('C:C', 80)

        await yandex_client.upload_file(upload_url, output.getvalue())

    return await yandex_client.publish_file(file_path)


async def create_project_report(
    session: AsyncSession,
    yandex_client: YandexDiskClient
) -> str:
    """Получить закрытые проекты, создать отчёт и вернуть ссылку."""
    projects = await (
        charity_project_repository.get_projects_by_completion_rate(session)
    )
    report_data = [
        {
            'name': project.name,
            'create_date': project.create_date,
            'close_date': project.close_date,
            'description': project.description
        }
        for project in projects
    ]
    return await create_simple_report(report_data, yandex_client)
