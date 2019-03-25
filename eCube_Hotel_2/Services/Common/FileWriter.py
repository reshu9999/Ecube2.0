import csv
class FileWriter:
    def WriteData(title,images,tables,links,category,prices,itemCode,info,filename):
        with open('E:/'+filename, 'w', encoding="utf-8") as csvfile:
            fieldnames = ['Name', 'values']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow({'Name': 'Title', 'values': title})
            writer.writerow({'Name': 'Images', 'values': images})
            writer.writerow({'Name': 'Tables', 'values': tables})
            writer.writerow({'Name': 'Links', 'values': links})
            writer.writerow({'Name': 'Category', 'values': category})
            if info and not info.isspace():
                writer.writerow({'Name': 'Info', 'values': info})
            writer.writerow({'Name': 'Prices', 'values': prices})
            writer.writerow({'Name': 'ItemNo', 'values': itemCode})




