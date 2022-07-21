from django.db import migrations


def create_base_creations_types(apps, schema_editor):
    CreationType = apps.get_model('creations', 'CreationType')

    types_map = [
        {'ru': 'Авторское право', 'en': 'Copyright', 'ps': 10, 'df': False, 'list': [
            {'ru': 'Произведение', 'en': 'Creative plot', 'ps': 100, 'df': True},
            {'ru': 'Музыкальное произведение', 'en': 'Musical composition', 'ps': 95, 'df': False},
            {'ru': 'Прототип (чертеж)', 'en': 'Prototype (blueprint)', 'ps': 90, 'df': False},
            {'ru': 'Логотип', 'en': 'Logo', 'ps': 85, 'df': False},
            {'ru': 'Литературное произведение', 'en': 'Literary work', 'ps': 80, 'df': False},
            {'ru': 'Учебный материал', 'en': 'Education material', 'ps': 75, 'df': False},
            {'ru': 'Фотография', 'en': 'Photo', 'ps': 70, 'df': False},
            {'ru': 'Видео', 'en': 'Video', 'ps': 65, 'df': False},
            {'ru': 'Сценарий', 'en': 'Scenario', 'ps': 60, 'df': False},
            {'ru': 'Программа ЭВМ', 'en': 'Computer program', 'ps': 55, 'df': False},
            {'ru': 'Персонаж', 'en': 'Character', 'ps': 50, 'df': False},
            {'ru': 'Рецептура', 'en': 'Recipe', 'ps': 45, 'df': False},
            {'ru': 'Изображение (Дизайн)', 'en': 'Image (design)', 'ps': 40, 'df': False},
            {'ru': 'Материал патентной заявки', 'en': 'Patent application material', 'ps': 35, 'df': False},
            {'ru': 'Технология (Методика)', 'en': 'Technology (Method)', 'ps': 30, 'df': False},
            {'ru': 'База данных', 'en': 'Database', 'ps': 25, 'df': False},
            {'ru': 'Фонограмма', 'en': 'Audio record', 'ps': 19, 'df': False},
            {'ru': 'Проектная документация', 'en': 'Project documentation', 'ps': 18, 'df': False},
            {'ru': 'Произведение науки', 'en': 'Work of science', 'ps': 17, 'df': False},
            {'ru': 'Научно-методическое произведение', 'en': 'Science education material', 'ps': 16, 'df': False},
        ]},
        {'ru': 'Коммерческая тайна', 'en': 'Trade secret', 'ps': 9, 'df': False, 'list': [
            {'ru': 'Ноу-хау (коммерческая тайна)', 'en': 'Know-how (trade secret)', 'ps': 20, 'df': False},
            {'ru': 'База данных клиентов', 'en': 'Client data base', 'ps': 15, 'df': False},
        ]},
        {'ru': 'Промышленная собственность', 'en': 'Industrial property', 'ps': 8, 'df': False, 'list': []},
        {'ru': 'Ноу-хау', 'en': 'Know-how', 'ps': 7, 'df': False, 'list': []},
        {'ru': 'Информация/Сведения', 'en': 'Research', 'ps': 6, 'df': False, 'list': []},
    ]

    for creation_type in types_map:
        parent_type = CreationType.objects.create(title=creation_type['ru'], title_en=creation_type['en'],
                                                  is_default=creation_type['df'], position=creation_type['ps'])
        for child_type in creation_type['list']:
            CreationType.objects.create(title=child_type['ru'], title_en=child_type['en'], parent=parent_type,
                                        is_default=child_type['df'], position=child_type['ps'])


class Migration(migrations.Migration):

    dependencies = [
        ('creations', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_base_creations_types),
    ]
