from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Categoria(models.Model):
    nome = models.CharField(_('name'), max_length=100)
    descrizione = models.TextField(_('description'), blank=True)

    class Meta:
        verbose_name_plural = _('Categories')
        ordering = ['nome']

    def __str__(self):
        return self.nome


class Prodotto(models.Model):
    nome = models.CharField(_('name'), max_length=200)
    descrizione = models.TextField(_('description'))
    quantita = models.PositiveIntegerField(_('quantity'), default=0)
    prezzo = models.DecimalField(_('price'), max_digits=10, decimal_places=2)
    immagine = models.ImageField(_('image'), upload_to='prodotti/', blank=True, null=True)
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='prodotti',
        verbose_name=_('category'),
    )
    data_inserimento = models.DateTimeField(_('date added'), default=timezone.now)
    data_aggiornamento = models.DateTimeField(_('date updated'), auto_now=True)

    class Meta:
        verbose_name_plural = _('Products')
        ordering = ['-data_inserimento']

    def __str__(self):
        return self.nome
