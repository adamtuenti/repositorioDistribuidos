import os
import shutil
ruta = os.getcwd()
print('%s' % ruta)
ruta_migrations="C:\\Users\\josea\\Desktop\\FenixEC\\"
#ruta_migrations = "C:\\Users\\Charles\\Desktop\\Educacion Continua\\Repositorio Integrado\\"
#ruta_migrations = "C:\\Users\\Luis Eduardo\\Desktop\\Educacion Continua\\Repositorio Integrado\\"

ruta_academico = ruta+"\\academico\\"
ruta_administrativo = ruta+"\\administrativo\\"
ruta_financiero = ruta+"\\financiero\\"
ruta_ventas = ruta+"\\ventas\\"

academico = [ruta_academico+ "diseño_evento\\", ruta_academico+"docente\\",ruta_academico+"evento\\"
,ruta_academico+"participante\\",ruta_academico+"plan_trabajo\\"]

administrativo = [ruta_administrativo+ "proveedores\\",ruta_administrativo+ "productos\\",ruta_administrativo+ "calificacion_proveedores\\",
ruta_administrativo+ "suministros\\"]

financiero = [ruta_financiero+ "orden_facturacion\\", ruta_financiero+"orden_ingreso\\",ruta_financiero+"orden_pago\\"
,ruta_financiero+"pago_eventos\\",ruta_financiero+"perfiles\\",ruta_financiero+"plan_anual_compras\\",ruta_financiero+"presupuestos\\"
,ruta_financiero+"presupuestos_anuales\\",ruta_financiero+"procesos_especiales\\"]

ventas =  [ruta_ventas+ "interesados\\", ruta_ventas+"personas_juridicas\\",ruta_ventas+"personas_naturales\\"
,ruta_ventas+"proformas\\",ruta_ventas+"propuesta_corp\\",ruta_ventas+"reporte_contacto\\",ruta_ventas+"seguimientos\\"]

def reemplaza_carpetasmigration(modulo):
    for carpeta in modulo:
        try:
            os.chdir(carpeta)
            shutil.rmtree("migrations\\")
            print('Si se borro')
        except OSError as e:
            print(e)
        try:
            os.chdir(ruta_migrations)
            shutil.copytree("migrations\\",carpeta+"migrations\\")
            print("Si se copio el migrations")
        except OSError as e:
            print(e)
    
reemplaza_carpetasmigration(academico)
reemplaza_carpetasmigration(ventas)
reemplaza_carpetasmigration(financiero)
reemplaza_carpetasmigration(administrativo)
