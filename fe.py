#!/usr/bin/python
# -*- coding: utf8 -*-
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 3, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTIBILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# for more details.

from pyafipws.wsaa import WSAA
from pyafipws.wsfev1 import WSFEv1
from pyafipws.pyfepdf import FEPDF
from tkt import ticket

"Ejemplo completo para WSFEv1 de AFIP (Factura Electrónica Mercado Interno)"

__author__ = "Mariano Reingart <reingart@gmail.com>"
__copyright__ = "Copyright (C) 2010 - 2019 Mariano Reingart"
__license__ = "GPL 3.0"

import os
import time
import sys
from decimal import Decimal
import datetime
import warnings
from configparser import ConfigParser


# Opciones de configuración (testing/homologación, cambiar para producción):
parser = ConfigParser()
parser.read('config.ini')

if parser.get('fiscal','homo'):
    URL_WSAA = "https://wsaahomo.afip.gov.ar/ws/services/LoginCms?wsdl"
    URL_WSFEv1 = "https://wswhomo.afip.gov.ar/wsfev1/service.asmx?WSDL"
else:
    URL_WSAA = "https://wsaa.afip.gov.ar/ws/services/LoginCms"
    URL_WSFEv1 = "https://servicios1.afip.gov.ar/wsfev1/service.asmx?WSDL"

CUIT = parser.get('fiscal','cuit')
CERT = parser.get('fiscal','cert')
PRIVATEKEY = parser.get('fiscal','privatekey')
CACHE = "../cache"
CONF_PDF = dict(
    LOGO=parser.get('fiscal','logo'),
    EMPRESA=parser.get('fiscal','empresa'),
    MEMBRETE1=parser.get('fiscal','domicilio'),
    MEMBRETE2="Buenos Aires",
    CUIT=parser.get('fiscal','cuit'),
    IIBB=parser.get('fiscal','iibb'),
    IVA=parser.get('fiscal','condicion_iva'),
    INICIO=parser.get('fiscal','inicio_actividades'),
)


def facturar(registros):
    """Rutina para emitir facturas electrónicas en PDF c/CAE AFIP Argentina"""

    # inicialización AFIP:
    wsaa = WSAA()
    wsfev1 = WSFEv1()
    # obtener ticket de acceso (token y sign):
    ta = wsaa.Autenticar(
        "wsfe", CERT, PRIVATEKEY, wsdl=URL_WSAA, cache=CACHE, debug=True
    )
    wsfev1.Cuit = CUIT
    wsfev1.SetTicketAcceso(ta)
    wsfev1.Conectar(CACHE, URL_WSFEv1)

    # inicialización PDF
    fepdf = FEPDF()
    fepdf.CargarFormato("factura.csv")
    fepdf.FmtCantidad = "0.2"
    fepdf.FmtPrecio = "0.2"
    fepdf.CUIT = CUIT
    for k, v in CONF_PDF.items():
        fepdf.AgregarDato(k, v)

    if "homo" in URL_WSAA:
        fepdf.AgregarCampo(
            "DEMO",
            "T",
            120,
            260,
            0,
            0,
            text="DEMOSTRACION",
            size=70,
            rotate=45,
            foreground=0x808080,
            priority=-1,
        )
        fepdf.AgregarDato("motivos_obs", "Ejemplo Sin validez fiscal")

    # recorrer los registros a facturar, solicitar CAE y generar el PDF:
    for reg in registros:
        hoy = datetime.date.today().strftime("%Y%m%d")
        cbte = Comprobante(
            tipo_cbte=6,
            punto_vta=4000,
            fecha_cbte=hoy,
            cbte_nro=reg.get("nro"),
            tipo_doc=96,
            nro_doc=reg["dni"],
            nombre_cliente=reg["nombre"],  # "Juan Perez"
            domicilio_cliente=reg["domicilio"],  # "Balcarce 50"
            fecha_serv_desde=reg.get("periodo_desde"),
            fecha_serv_hasta=reg.get("periodo_hasta"),
            fecha_venc_pago=reg.get("venc_pago", hoy),
        )

        for renglon in reg["items"]:
            cbte.agregar_item(
                ds=renglon["descripcion"],
                qty=renglon["cantidad"],
                precio=renglon["precio"],
                tasa_iva=renglon["tasa_iva"]

        )


        cbte.encabezado["imp_total"] = round(cbte.encabezado["imp_total"],2)
        cbte.encabezado["imp_iva"] = round(cbte.encabezado["imp_iva"],2)
        #cbte.encabezado["imp_total"] = round(cbte.encabezado["imp_total"],2)
        
        ok = cbte.autorizar(wsfev1)
        nro = cbte.encabezado["cbte_nro"]
        print("Factura autorizada", nro, cbte.encabezado["cae"])
        if "homo" in URL_WSFEv1:
            cbte.encabezado["motivos_obs"] = "Ejemplo Sin validez fiscal"
        
        #desactivo estas 2 lineas para probar con el ticket
        #ok = cbte.generar_pdf(fepdf, "factura_{}.pdf".format(nro)) #en factura_{}.pdf agregar antes un path para que queden las facturas organizadas
        #print("PDF generado", ok)
        ticket(cbte)



class Comprobante:
    def __init__(self, **kwargs):
        self.encabezado = dict(
            tipo_doc=99,
            nro_doc=0,
            tipo_cbte=6,
            cbte_nro=None,
            punto_vta=4000,
            fecha_cbte=None,
            imp_total=0.00,
            imp_tot_conc=0.00,
            imp_neto=0.00,
            imp_trib=0.00,
            imp_op_ex=0.00,
            imp_iva=0.00,
            moneda_id="PES",
            moneda_ctz=1.000,
            obs="Observaciones Comerciales, libre",
            concepto=1,
            fecha_serv_desde=None,
            fecha_serv_hasta=None,
            fecha_venc_pago=None,
            nombre_cliente="",
            domicilio_cliente="",
            localidad="",
            provincia="",
            pais_dst_cmp=200,
            id_impositivo="Consumidor Final",
            forma_pago="30 dias",
            obs_generales="Observaciones Generales<br/>linea2",
            obs_comerciales="Observaciones Comerciales<br/>texto libre",
            motivo_obs="",
            cae="",
            resultado="",
            fch_venc_cae="",
        )
        self.encabezado.update(kwargs)
        if self.encabezado["fecha_serv_desde"] or self.encabezado["fecha_serv_hasta"]:
            self.encabezado["concepto"] = 3  # servicios
        else:
            self.encabezado["fecha_venc_pago"]=None

        self.cmp_asocs = []
        self.items = []
        self.ivas = {}

    def agregar_item(
        self,
        ds="Descripcion del producto P0001",
        qty=1,
        precio=0,
        tasa_iva=21.0,
        umed=7,
        codigo="P0001",
    ):
        """Agregar producto / servicio facturado (calculando IVA)"""
        # detalle de artículos:
        item = dict(
            u_mtx=123456,
            cod_mtx=1234567890123,
            codigo=codigo,
            ds=ds,
            qty=qty,
            umed=umed,
            bonif=0.00,
            despacho=u"Nº 123456",
            dato_a="Dato A",
        )
        subtotal = precio * qty
        if tasa_iva:
            iva_id = {10.5: 4, 0: 3, 21: 5, 27: 6}[tasa_iva]
            item["iva_id"] = iva_id
            item["tasa_iva"] = tasa_iva
            # discriminar IVA si es clase A / M
            iva_liq = subtotal * tasa_iva / 100.0
            self.agergar_iva(iva_id, subtotal, iva_liq)
            self.encabezado["imp_neto"] += subtotal
            self.encabezado["imp_iva"] += iva_liq
            if self.encabezado["tipo_cbte"] in (
                1,
                2,
                3,
                4,
                5,
                34,
                39,
                51,
                52,
                53,
                54,
                60,
                64,
            ):
                item["precio"] = round(precio / (1.0 + tasa_iva / 100.0),2)
                item["imp_iva"] = round(importe * (tasa_iva / 100.0),2)
            else:
                # no discriminar IVA si es clase B (importe final iva incluido)
                item["precio"] = round(precio * (1.0 + tasa_iva / 100.0),2)
                item["imp_iva"] = None
                subtotal += iva_liq
                iva_liq = 0
        else:
            item["precio"] = precio
            item["imp_iva"] = None
            if tasa_iva is None:
                self.encabezado["imp_tot_conc"] += subtotal  # No gravado
            else:
                self.encabezado["imp_op_ex"] += subtotal  # Exento
        item["importe"] = subtotal
        self.encabezado["imp_total"] += round(subtotal + iva_liq,2)
        self.items.append(item)

    def agergar_iva(self, iva_id, base_imp, importe):
        iva = self.ivas.setdefault(
            iva_id, dict(iva_id=iva_id, base_imp=0.0, importe=0.0)
        )
        iva["base_imp"] += base_imp
        iva["importe"] += round(importe,2) #este fue el round del AlicIva

    def autorizar(self, wsfev1):
        "Prueba de autorización de un comprobante (obtención de CAE)"

        # datos generales del comprobante:
        if not self.encabezado["cbte_nro"]:
            # si no se especifíca nro de comprobante, autonumerar:
            ult = wsfev1.CompUltimoAutorizado(
                self.encabezado["tipo_cbte"], self.encabezado["punto_vta"]
            )
            self.encabezado["cbte_nro"] = int(ult) + 1

        self.encabezado["cbt_desde"] = self.encabezado["cbte_nro"]
        self.encabezado["cbt_hasta"] = self.encabezado["cbte_nro"]
        wsfev1.CrearFactura(**self.encabezado)

        # agrego un comprobante asociado (solo notas de crédito / débito)
        for cmp_asoc in self.cmp_asocs:
            wsfev1.AgregarCmpAsoc(**cmp_asoc)

        # agrego el subtotal por tasa de IVA (iva_id 5: 21%):
        for iva in self.ivas.values():
            wsfev1.AgregarIva(**iva)

        # llamo al websevice para obtener el CAE:
        # PODRIA PREGUNTAR SI NO MANDO EL CAE Y YA ESTA EN LA CABECERA, ENTONCES NO LO PIDO, PORQUE
        # PODRIA USARLO PARA REIMPRIMIR UNA FACTURA GUARDADA EN UNA BASE DE DATOS
        wsfev1.CAESolicitar()

        if wsfev1.ErrMsg:
            raise RuntimeError(wsfev1.ErrMsg)

        for obs in wsfev1.Observaciones:
            warnings.warn(obs)

        assert wsfev1.Resultado == "A"  # Aprobado!
        assert wsfev1.CAE
        assert wsfev1.Vencimiento

        self.encabezado["resultado"] = wsfev1.Resultado
        self.encabezado["cae"] = wsfev1.CAE
        self.encabezado["fch_venc_cae"] = wsfev1.Vencimiento
        return True

    def generar_pdf(self, fepdf, salida="/tmp/factura.pdf"):

        fepdf.CrearFactura(**self.encabezado)

        # completo campos extra del encabezado:
        ok = fepdf.EstablecerParametro(
            "localidad_cliente", self.encabezado["localidad"]
        )
        ok = fepdf.EstablecerParametro(
            "provincia_cliente", self.encabezado["provincia"]
        )

        # imprimir leyenda "Comprobante Autorizado" (constatar con WSCDC!)
        ok = fepdf.EstablecerParametro("resultado", self.encabezado["resultado"])

        # detalle de artículos:
        for item in self.items:
            fepdf.AgregarDetalleItem(**item)

        # agrego remitos y otros comprobantes asociados:
        for cmp_asoc in self.cmp_asocs:
            fepdf.AgregarCmpAsoc(**cmp_asoc)

        # agrego el subtotal por tasa de IVA (iva_id 5: 21%):
        for iva in self.ivas.values():
            fepdf.AgregarIva(**iva)

        # armar el PDF:
        fepdf.CrearPlantilla(papel="A4", orientacion="portrait")
        fepdf.ProcesarPlantilla(num_copias=1, lineas_max=24, qty_pos="izq")
        fepdf.GenerarPDF(archivo=salida)
        return salida


if __name__ == "__main__":
    # TODO: leer comprobantes de planilla CSV
    # Ejemplo para facturación masiva por programa:
    # IMPORTANTE: es recomendable indicar el nro de factura (y guardarlo antes)
    # para evitar generar varias facturas distintas para el mismo registro, y
    # poder recuperarlas (reproceso automático) si hay falla de comunicación

    facturas = [ {"dni": 1, "nombre": "", "domicilio": "",
                "items": [{"descripcion":"Tomate", "cantidad":2, "precio": 165.5, "tasa_iva": 21},
                          {"descripcion":"Fideos", "cantidad":2, "precio": 413, "tasa_iva": 21}]} ] 


    datos_factura = {"dni": 1, 
    "items" : [{"departamento":"almacen","cantidad":1,"precio": 125.50,"tasa_iva": 21},
        {"departamento":"verduleria","cantidad":1,"precio": 525.50,"tasa_iva": 10.5},
        {"departamento":"cigarrillos","cantidad":1,"precio": 325.50,"tasa_iva": 10.5}] }


    
    facturar(facturas)
