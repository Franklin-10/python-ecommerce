from typing import Any
from django.db import models
from PIL import Image
from django.conf import settings
import os
from utils.rands import slugify_new
from utils.utils import formata_preco


# Create your models here.

class Produto(models.Model):
    nome = models.CharField(max_length=255)
    descricao_curta = models.TextField(max_length=255)
    descricao_longa = models.TextField()
    imagem = models.ImageField(upload_to='produto_imagens/%Y/%m/')
    slug = models.SlugField(unique=True, blank=True)
    preco_exibicao = models.FloatField(verbose_name='Preço')
    preco_promocional = models.FloatField(verbose_name='Preço Promocional', blank=True, default=0)
    tipo = models.CharField(
        default='V', 
        max_length=1, 
        choices=(
            ('V', 'Variação'),
            ('S', 'Simples'),
        )
    )

    def get_preco_formatado(self):
        return formata_preco(self.preco_exibicao)
    get_preco_formatado.short_description = 'Preço'
    
    def get_preco_promocional_formatado(self):
        return formata_preco(self.preco_promocional)
    get_preco_promocional_formatado.short_description = 'Preço Promo.'

    @staticmethod
    def resize_image(img, new_width=800):
        img_fullpath = os.path.join(settings.MEDIA_ROOT, img.name)
        img_pil = Image.open(img_fullpath)
        original_width, original_height = img_pil.size
        
        if original_width <= new_width:
            print('largura original menor que nova largura')
            return 
        
        new_height = round((new_width * original_height) / original_width)

        new_img = img_pil.resize((new_width, new_height), Image.LANCZOS) ##type:ignore
        new_img.save(
            img_fullpath,
            optimize=True,
            quality=50
        )
        print('Imagem redimensionada')
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_new(self.nome, 4)
        super().save(*args, **kwargs)

        max_image_size = 800

        if self.imagem:
            self.resize_image(self.imagem, max_image_size)

    def __str__(self):
        return self.nome

class Variacao(models.Model):
    class Meta:
        verbose_name = 'Variação'
        verbose_name_plural = 'Variações'

    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    nome = models.CharField(max_length=50, blank=True, null=True)
    preco = models.FloatField()
    preco_promocional = models.FloatField(default=0)
    estoque = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return self.nome or self.produto.nome