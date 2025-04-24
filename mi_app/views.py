from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import xml.etree.ElementTree as ET

@csrf_exempt  # Deshabilita la verificación CSRF para pruebas locales
def process_xml(request):
    if request.method == "POST":
        try:
            xml_content = request.body
            
           
            root = ET.fromstring(xml_content.decode("utf-8"))

            # Definición del espacio de nombres
            namespace = {
                'cac': 'urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2',
                'cbc': 'urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2',
                'cdt': 'urn:DocumentInformation:names:specification:ubl:colombia:schema:xsd:DocumentInformationAggregateComponents-1',
                'chl': 'urn:carvajal:names:specification:ubl:colombia:schema:xsd:CarvajalHealthComponents-1',
                'clm54217': 'urn:un:unece:uncefact:codelist:specification:54217:2001',
                'clm66411': 'urn:un:unece:uncefact:codelist:specification:66411:2001',
                'clmIANAMIMEMediaType': 'urn:un:unece:uncefact:codelist:specification:IANAMIMEMediaType:2003',
                'cts': 'urn:carvajal:names:specification:ubl:colombia:schema:xsd:CarvajalAggregateComponents-1',
                'ds': 'http://www.w3.org/2000/09/xmldsig#',
                'ext': 'urn:oasis:names:specification:ubl:schema:xsd:CommonExtensionComponents-2',
                'grl': 'urn:General:names:specification:ubl:colombia:schema:xsd:GeneralAggregateComponents-1',
                'ipt': 'urn:DocumentInformation:names:specification:ubl:colombia:schema:xsd:InteroperabilidadPT-1',
                'qdt': 'urn:oasis:names:specification:ubl:schema:xsd:QualifiedDatatypes-2',
                'sts': 'dian:gov:co:facturaelectronica:Structures-2-1',
                'udt': 'urn:un:unece:uncefact:data:specification:UnqualifiedDataTypesSchemaModule:2',
                'xades': 'http://uri.etsi.org/01903/v1.3.2#',
                'xades141': 'http://uri.etsi.org/01903/v1.4.1#',
                'xsi': 'http://www.w3.org/2001/XMLSchema-instance'
            }

            # Procesar los datos XML
            descripcion = root.find('.//cac:Attachment/cac:ExternalReference/cbc:Description', namespace)
            tipoDocumento = "NC"
            if descripcion is not None and "Invoice xmlns" in descripcion.text:
                tipoDocumento = "FE"

            nitEmisor = root.find('.//cac:SenderParty//cbc:CompanyID', namespace)
            nitDeudor = root.find('.//cac:ReceiverParty//cbc:CompanyID', namespace)
            nombreProveedor = root.find('.//cac:SenderParty//cbc:RegistrationName', namespace)
            fechaDocumento = root.find('.//cbc:IssueDate', namespace)
            numeroFactura = root.find('.//cbc:ParentDocumentID', namespace)

            return JsonResponse({
                "tipoDocumento": tipoDocumento,
                "nitEmisor": nitEmisor.text.strip() if nitEmisor is not None else None,
                "nitDeudor": nitDeudor.text.strip() if nitDeudor is not None else None,
                "nombreProveedor": nombreProveedor.text.strip() if nombreProveedor is not None else None,
                "fechaDocumento": fechaDocumento.text.strip() if fechaDocumento is not None else None,
                "numeroFactura": numeroFactura.text.strip() if numeroFactura is not None else None,
            })
        
        except ET.ParseError:
            return JsonResponse({"error": "Formato XML inválido"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Método no permitido"}, status=405)
