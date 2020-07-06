from src.models import pharmacyModel, labModel

def getPharmacyInvoice(invoiceId):
    invoiceItemId = pharmacyModel.PharmacyInvoice.objects(id = invoiceId).first()        
    medicalItems = list()
    invoice = list()            
    for item in invoiceItemId.items:
        itemInventory = pharmacyModel.PahrmacyInventory.objects(id=item['id']).first()           
        medicalItems.append({
            'name': itemInventory.name,
            'price': itemInventory.price,
            'quantity': item['quantity']
        })
    invoice = {
        'date': invoiceItemId['date'],
        'items': medicalItems,
        'total': invoiceItemId['total']
        } 

    return invoice

def getPharmacyInvoices(inoviceIdsList):
    invoices = list()
    if (isinstance(inoviceIdsList, str) ):
        invoices.append(getPharmacyInvoice(inoviceIdsList))
        return invoices

    for invoiceId in inoviceIdsList:
        invoices.append(getPharmacyInvoice(invoiceId))     

    return invoices



def getLabInvoice(invoiceId):
    invoiceItemId = labModel.LabInvoice.objects(id = invoiceId).first()        
    labItems = list()
    invoice = list() 
         
    for item in invoiceItemId.items:
        itemInventory = labModel.LabInventory.objects(id=item).first()           
        labItems.append({
            'name': itemInventory.name,
            'price': itemInventory.price,
        })
    invoice = {
        'date': invoiceItemId['date'],
        'items': labItems,
        'total': invoiceItemId['total']
        } 

    return invoice





def getLabInvoices(inoviceIdsList):
    invoices = list()
    if (isinstance(inoviceIdsList, str) ): 
        invoices.append(getLabInvoice(inoviceIdsList))       
        return invoices

    for invoiceId in inoviceIdsList:
        invoices.append(getLabInvoice(invoiceId))     

    return invoices
            
        
        
