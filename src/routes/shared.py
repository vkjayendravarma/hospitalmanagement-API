from src.models import pharmacyModel


def getPharmacyInvoices(inoviceIdsList):
    invoices = list()
    for invoiceId in inoviceIdsList:
        invoiceItemId = pharmacyModel.PharmacyInvoice.objects(id = invoiceId).first()
        
        medicalItems = list()
        
        for item in invoiceItemId.items:
            itemInventory = pharmacyModel.PahrmacyInventory.objects(id=item['id']).first()           
            medicalItems.append({
                'name': itemInventory.name,
                'price': itemInventory.price,
                'quantity': item['quantity']
            })
        
        
        invoices.append({
            'date': invoiceItemId['date'],
            'items': medicalItems,
            'total': invoiceItemId['total']
            })
    return invoices
            
        
        
