from django.db import migrations


def copy_to_english_fields(apps, schema_editor):
    Prodotto = apps.get_model('myapp', 'Prodotto')
    Categoria = apps.get_model('myapp', 'Categoria')

    for p in Prodotto.objects.all():
        if not p.nome_en and p.nome:
            p.nome_en = p.nome
        if not p.descrizione_en and p.descrizione:
            p.descrizione_en = p.descrizione
        p.save()

    for c in Categoria.objects.all():
        if not c.nome_en and c.nome:
            c.nome_en = c.nome
        if not c.descrizione_en and c.descrizione:
            c.descrizione_en = c.descrizione
        c.save()


class Migration(migrations.Migration):
    dependencies = [
        ('myapp', '0003_alter_categoria_options_alter_prodotto_options_and_more'),
    ]

    operations = [
        migrations.RunPython(copy_to_english_fields),
    ]
