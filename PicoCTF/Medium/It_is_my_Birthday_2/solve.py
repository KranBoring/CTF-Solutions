from pypdf import PdfMerger

pdf = "invite.pdf"
payloads = ["shattered-1.pdf","shattered-2.pdf"]

merger1 = PdfMerger()
merger2 = PdfMerger()

merger1.append(pdf)
merger1.append(payloads[0])

merger2.append(pdf)
merger2.append(payloads[1])

merger1.write("invite1.pdf")
merger2.write("invite2.pdf")