import PyPDF2 as pypdf
import textract
import re
import os
import json

def get_page_content(file_name,start_page_num=0,end_page_num=0):
    with open(file_name, 'rb') as pdf:
        pdf_file = pypdf.PdfFileReader(pdf)
        total_pages = pdf_file.numPages
        if not(0<=start_page_num<=total_pages and 0<=end_page_num<=total_pages ):
            return None
        else:
            page_text=""
            if start_page_num ==0 and end_page_num==0:
                start_at = 1
                end_at = total_pages
            else:
                start_at = start_page_num-1
                end_at = end_page_num
            for page_num in range(start_at,end_at):
                page = pdf_file.getPage(page_num)
                page_text+= page.extractText()
            return page_text

def split_pdf(file_name,start_page,end_page,output_file):
    with open(file_name,"rb") as my_pdf:
        pdf_file = pypdf.PdfFileReader(my_pdf)
        total_pages = pdf_file.numPages
        if not(0<=start_page<total_pages and 0<=end_page<total_pages and start_page<=end_page):
            return None
        else:
            pdfWriter = pypdf.PdfFileWriter()
            for page_num in range(start_page-1,end_page):
                pdfWriter.addPage(pdf_file.getPage(page_num))
            with open(output_file,"wb") as output_pdf:
                pdfWriter.write(output_pdf)

        
def get_text_from_scanned_pdf(file_name):
    extracted_text = textract.process(file_name, method='tesseract', language='eng')
    return extracted_text

def put_pages_to_text(mainfile,start_page_num,end_page_num):
    split_pdf(mainfile,start_page_num,end_page_num,"temp.pdf")
    my_text = get_text_from_scanned_pdf("temp.pdf")
    os.remove("temp.pdf")
    with open(mainfile+"_page_"+str(start_page_num)+"_to_"+str(end_page_num),"wb") as output_text:
        output_text.write(my_text)

def single_page_to_text(mainfile,page_num):
    put_pages_to_text(mainfile,page_num,page_num)
        
        
def parse_text_content(text_file):
    with open(text_file,"r") as t_file:
        texual_data = t_file.readlines()
    data = {}
    parent = ""
    flag = 0
    content = ""
    regex_pattern = "^\d[\.|,]\s\w*"
    for line in texual_data:
        if flag==1 and re.match(regex_pattern,line):
            flag=0
            all_text = content.split("\n")
            temp = ""
            for i in range(len(all_text)-1):
                temp+=all_text[i]
                if all_text[i+1]=="" or all_text[i+1]==" ":
                    if temp.strip()!="":
                        data[parent].append(temp)
                    temp = ""
            content = ""
        if re.match("\d+\.\d+.*",line):
            for key in data:
                if key.split(".")[0] == line.split(".")[0]:
                    data[key].append(line.strip())
        else:
            content+=line
        if flag==0 and re.match(regex_pattern,line):
            flag=1
            parent = line.strip().replace(",",".",1)
            data[parent] = []
            content = ""
    return data

def merge_similar_A_Levels_paper_into_one():
    current_dir = os.getcwd()
    data = ""
    with open("subjects.json") as f:
        data = json.load(f)
    
    all_dirs = [os.path.join(current_dir,sub) for sub in data["subjects"]]

    paper_types_gathered = {}
    
    with open("errlog.txt","w") as o:
        pass
    

    for dir in all_dirs:
        #empty the paper types first
        for i in range(8):
            paper_types_gathered[str(i)]=[] 
         
        for file_name in os.listdir(dir):
            if file_name.endswith(".pdf"):
                tokens = re.split("_|\.",file_name)
                if len(tokens)==5:
                    subject_code = tokens[0]
                    paper_type = tokens[3][0]
                    qp_or_ms = tokens[2]
                    if qp_or_ms=="qp":
                        if paper_type.isnumeric():
                            paper_types_gathered[paper_type].append(file_name)


        for key in paper_types_gathered:
            pdfWriter = pypdf.PdfFileWriter()
            paper_types_gathered[key].sort()
            for item in paper_types_gathered[key]:
                try:
                    ms_of_current_paper = re.sub("qp","ms",item)
                    qp_file_to_read = open(os.path.join(dir,item),"rb")
                    ms_file_to_read = open(os.path.join(dir,ms_of_current_paper),"rb")
                    pdf_qp_file = pypdf.PdfFileReader(qp_file_to_read)
                    pdf_ms_file = pypdf.PdfFileReader(ms_file_to_read)
                    total_pages = pdf_qp_file.numPages
                    for page_num in range(0,total_pages):
                        pdfWriter.addPage(pdf_qp_file.getPage(page_num))
                    total_pages = pdf_ms_file.numPages
                    for page_num in range(1,total_pages):
                        pdfWriter.addPage(pdf_ms_file.getPage(page_num))
                    print(f"Read from {item} successfully")
                except:
                    print(f"Failed to read content from {item}")
                    with open("errlog.txt","a") as errlog:
                        errlog.write(f"Failed to write  content for {item}\n")
                        continue
            write_file = open(os.path.join(dir,f"{key}.pdf"),"wb")
            pdfWriter.write(write_file)
            write_file.close()
            

def run_program():
    all_data = parse_text_content("chemistry_syllabus.txt")
    print(all_data)
    for key in all_data:
        with open("managed_syllabus.txt","a") as write_file:
            write_file.write(key+":\n")
            print("Written:"+key)
            for elements in all_data[key]:
                write_file.write("\t"+elements+"\n")
                print("Written:"+elements)
    
        
def extract_a_levels_questions(text,file_name):
    text = re.sub("(\w)\\n(\w)","\\1\\2",text)
    #print(repr(text))
    subject_code = file_name.split("_")[0]
    regex_biology_P1 ="(?:\n\d+\n\s(\w.*?)\?)|(?:\n\d+\s\n(\w.*?)\?)"
    regex_chemistry_P1 = "(?:\n\d+\s(\w.*?)\?)|(?:\n\[Turn\sover\s\d+\s(\w.*?)\?)|(?:\n\s\d+\s(\w.*?)\?)"
    if subject_code=="9701":
        regex_pattern = regex_chemistry_P1
    elif subject_code=="9700":
        regex_pattern = regex_biology_P1

    return re.findall(regex_pattern,text,flags=re.DOTALL)


if __name__ == '__main__':
    merge_similar_A_Levels_paper_into_one()
    



