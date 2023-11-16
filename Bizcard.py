import pandas as pd
import streamlit as st
import easyocr
import base64
from streamlit_option_menu import option_menu
from PIL import Image
import re
import psycopg2 as pg2
import pandas as pd
import json
import webbrowser
import time

st.set_page_config(page_title='Bizcard',layout='wide')


# Database Creation
mydb = pg2.connect(host='localhost', user='postgres', port='5433', password='bhadri@0121', database='bizcard')
mycurser=mydb.cursor()

# Background Image
def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
        f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
        unsafe_allow_html=True
    )
add_bg_from_local('/Users/bhadrinathboddu/Documents/Guvi/BizcardX/Images/bg1.avif')

st.title("BizCardX : Extracting Business Card Data with OCR")

#Option Menu
st.markdown('##')
opt1,opt2,opt3=st.columns([1,150,1])
with opt2:
    selected=option_menu(menu_title='', options=['Home','Card','Records','Update','Delete','Download','Connect'],icons=['house','card-heading','file-earmark','pencil-square','trash','download',''],orientation='horizontal'
                ,styles={
                "container": { "background-color": "#0d0c0c"},
                "icon": {"color": "white", "font-size": "18px"},
                "nav-link": {"font-size": "18px", "text-align": "left", "margin":"0px", "--hover-color": "#3333b5"},
                "nav-link-selected": {"background-color": "#3333b5"}  })

if selected=='Home':
    st.markdown("<h2 style= 'color: white;font-size: 40px;'>Problem Statement </h2>",
        unsafe_allow_html=True)
    h1,h2,h3=st.columns([2,0.3,1])
    with h1:
        st.markdown('''<p style= 'color: white;font-size: 16px;text-align: justify;'>
                Streamlit application that allows users to
                upload an image of a business card and extract relevant information from it using
                easyOCR. The extracted information should include the company name, card holder
                name, designation, mobile number, email address, website URL, area, city, state,
                and pin code. The extracted information should then be displayed in the application's
                graphical user interface (GUI).</br>In addition, the application should allow users to save the extracted information into
                a database along with the uploaded business card image. The database should be
                able to store multiple entries, each with its own business card image and extracted
                information.</p>''',
                    unsafe_allow_html=True)
        st.markdown(
            "<h2 style= 'color: white;font-size: 30px;'>More Information About OCR</h2>",
            unsafe_allow_html=True)
        url = 'https://pypi.org/project/easyocr/'

        if st.button('Click Here'):
            webbrowser.open_new_tab(url)
    with h3:
        st.image('/Users/bhadrinathboddu/Documents/Guvi/BizcardX/Images/card2.jpeg')

                                        #Card
elif selected=='Card':
    try:
        st.markdown(
            "<h2 style= 'color: white;font-size: 40px;'>BizCard to Text</h2>",
            unsafe_allow_html=True)
        file1,file2,file3=st.columns([1,4,1])
        with file2:
            uploaded_files = st.file_uploader("Choose the Card", accept_multiple_files=True)
        col1,col2,col3 = st.columns([2,0.3,2])
        with col1:
            st.image(uploaded_files)
        with col3:
                c1,c3,c2=st.columns([2,0.2,1.8])
                st.write('')
                if "Extract" not in st.session_state:
                    st.session_state["Extract"] = False
                if "Insert DataBase" not in st.session_state:
                    st.session_state["Insert DataBase"] = False
                with c1:
                    st.markdown("<h2 style= 'color: white;font-size: 30px;'>Click to Extract the Card</h2>",
                                unsafe_allow_html=True)
                    if st.button("Extract"):
                        st.session_state["Extract"] = not st.session_state["Extract"]
                    if st.session_state["Extract"]:
                        reader=easyocr.Reader(['en'])
                        result=reader.readtext(f'/Users/bhadrinathboddu/Documents/Guvi/BizcardX/Cards/{uploaded_files[0].name}'.format(uploaded_files[0].name))
                        detlst=[]
                        for i in range(len(result)):
                            detlst.append(result[i][1])
                        details=' '.join(detlst)
                        st.write('#')
                        name=result[0][1]
                        role=result[1][1]
                        webres=res = re.findall(r'(www|WWW|wWW)(\s|)(\.?[A-Z]+|\.?[a-z]+|\.?[A-Z][a-z]+).?(\.com|uncom)', details)
                        weblst = []
                        for i in webres[0]:
                            weblst.append(i)
                        website = ''.join(weblst)
                        newweb=website.replace(' ','.')
                        maildet = re.findall(r'([a-z]+)(@)([a-z]+|[A-Z]+[0-9]|[A-Z][a-z]+|[A-Z]+)(\.com)', details)
                        mailst = []
                        for i in maildet[0]:
                            mailst.append(i)
                        mail=''.join(mailst)
                        phone=re.findall(r'[0-9]+-[0-9]{3}-[0-9]{4}',details)
                        state=re.findall(r'[A-Z][a-z]+[A-Z][a-z]+',details)
                        pin=re.findall(r'[0-9]+',details)
                        pinlst = [int(i) for i in pin]
                        pinlst.sort()
                        pincode=str(pinlst[-1])
                        streetdet=re.findall(r'([0-9]{3})\s([A-Z]+)\s(St|Street)',details)
                        streetlst = []
                        for i in streetdet[0]:
                            streetlst.append(i)
                        street = ' '.join(streetlst)
                        districtdet = re.findall(r'(,?\s[A-Z][a-z]+|,?\s[A-Z]+)(,|;)\s', details)
                        districtcon = ' '
                        for i in districtdet[0]:
                            districtcon += i
                        district=districtcon.replace(';', '').replace(',','').replace(' ','')
                        st.markdown(
                            "<h2 style= 'color: white;font-size: 30px;'>Details about {}</h2>".format(name),
                            unsafe_allow_html=True)
                        st.markdown(
                            "<h2 style= 'color: white;font-size: 22px;'>Name : {}</h2>".format(name),
                            unsafe_allow_html=True)
                        st.markdown(
                            "<h2 style= 'color: white;font-size: 22px;'>Designation : {}</h2>".format(role),
                            unsafe_allow_html=True)
                        st.markdown(
                            "<h2 style= 'color: white;font-size: 22px;'>Website : {}</h2>".format(newweb),
                            unsafe_allow_html=True)
                        st.markdown(
                            "<h2 style= 'color: white;font-size: 22px;'>Mail : {}</h2>".format(mail),
                            unsafe_allow_html=True)
                        if len(phone)==1:
                            st.markdown(
                                "<h2 style= 'color: white;font-size: 22px;'>Phone : {}</h2>".format(phone[0]),
                                unsafe_allow_html=True)
                        elif len(phone)==2:
                            st.markdown(
                                "<h2 style= 'color: white;font-size: 22px;'>Phone : {}</h2>".format(phone[0]),
                                unsafe_allow_html=True)
                            st.markdown(
                                "<h2 style= 'color: white;font-size: 22px;'>Phone : {}</h2>".format(phone[1]),
                                unsafe_allow_html=True)
                        st.markdown(
                            "<h2 style= 'color: white;font-size: 22px;'>Street : {}</h2>".format(street),
                            unsafe_allow_html=True)
                        st.markdown(
                            "<h2 style= 'color: white;font-size: 22px;'>District : {}</h2>".format(district),
                            unsafe_allow_html=True)
                        st.markdown(
                            "<h2 style= 'color: white;font-size: 22px;'>State : {}</h2>".format(state[0]),
                            unsafe_allow_html=True)
                        st.markdown(
                            "<h2 style= 'color: white;font-size: 22px;'>Pincode : {}</h2>".format(pincode),
                            unsafe_allow_html=True)


                        dic={'Name':name,'Designation':role,'Website':newweb,'Mail':mail,'Phone':phone[0],'Street':street,'District':district,'State':state[0],'Pincode':pincode}
                with c2:
                    st.markdown("<h2 style= 'color: white;font-size: 30px;'>Insert into DataBase</h2>",
                                unsafe_allow_html=True)
                    if st.button('Insert DataBase'):
                        st.write('')
                        insert = 'insert into person values(%s,%s,%s,%s,%s,%s,%s,%s,%s)'
                        val = (dic['Name'], dic['Designation'], dic['Website'], dic['Mail'], dic['Phone'], dic['Street'],
                               dic['District'], dic['State'], dic['Pincode'])
                        mycurser.execute(insert, val)
                        mydb.commit()
                        with st.spinner('Waiting for Confirmation...'):
                            time.sleep(2)
                            st.success('Record Insert Sucessfully !')
    except:
        st.write('')

                                    #Records


elif selected=='Records':
    try:
        st.markdown("<h2 style= 'color: white;font-size: 40px;'>DataBase Records</h2>",
                    unsafe_allow_html=True)
        st.markdown('#')
        namequery='select Name from person'
        namelst=[]
        mycurser.execute(namequery)
        nameresult=mycurser.fetchall()
        for i in nameresult:
            namelst.append(i[0])
        namec1,namec2,namec3=st.columns([0.8,2,0.8])
        with namec2:
            recordname=st.selectbox('Choose the Name',namelst)
        select = "select * from person where Name= '{}'".format(recordname)
        mycurser.execute(select)
        val = mycurser.fetchall()
        dic={'Name':val[0][0],'Designation':val[0][1],'Website':val[0][2],'Mail':val[0][3],'Phone':val[0][4],'Street':val[0][5],'District':val[0][6],'State':val[0][7],'Pincode':val[0][8]}
        dfc1,dfc2,dfc3=st.columns([0.5,2,0.5])
        with dfc2:
            sp1,sp2,sp3=st.columns([1,1,1])
            with sp2:
                st.markdown('#')
                with st.spinner('Please Wait . . .'):
                    time.sleep(2)
            df=pd.DataFrame(dic,index=[0])
            st.markdown(
                "<h2 style= 'color: white;font-size: 25px;'>Record of {}</h2>".format(dic['Name']),
                unsafe_allow_html=True)
            st.write('')
            st.write('')
            st.write(df)
    except Exception as e:
        st.markdown('#')
        st.error(f'An error occurred: {str(e)}')

            #Update

elif selected=='Update':
    try:
        st.markdown('#')
        st.markdown("<h2 style= 'color: white;font-size: 40px;'>Update the Record</h2>",
                    unsafe_allow_html=True)
        st.markdown('#')
        namequery = 'select Name from person'
        namelst = []
        mycurser.execute(namequery)
        nameresult = mycurser.fetchall()
        for i in nameresult:
            namelst.append(i[0])
        up1, up2, up3 = st.columns([0.4, 2, 0.3])
        with up2:
            selectname=st.selectbox('Choose the Name',namelst)
        st.write('#')
        c1,col1,col2=st.columns([1,2,1])
        c2,col3, col4 = st.columns([1,2,1])
        c3,col5, col6 = st.columns([1,2,1])
        c4,col7, col8 = st.columns([1,2,1])
        c5,col9, col10 = st.columns([1,2,1])
        c6,col11, col12 = st.columns([1,2,1])
        c7,col13, col14 = st.columns([1,2,1])
        c8,col15, col16 = st.columns([1,2,1])
        c9,col17, col18 = st.columns([1,2,1])
        st.write('#')
        with col1:
            upname=st.text_input('Name',selectname)
        desquery = "select designation from person where Name='{}'".format(selectname)
        mycurser.execute(desquery)
        desres=mycurser.fetchall()
        with col3:
            updes=st.text_input('Designation',desres[0][0])
        webquery="select website from person where Name='{}'".format(selectname)
        mycurser.execute(webquery)
        webres = mycurser.fetchall()
        with col5:
            upweb = st.text_input('Website', webres[0][0])
        mailquery = "select mail from person where Name='{}'".format(selectname)
        mycurser.execute(mailquery)
        mailres = mycurser.fetchall()
        with col7:
            upmail = st.text_input('Mail-ID', mailres[0][0])
        phoquery = "select phone from person where Name='{}'".format(selectname)
        mycurser.execute(phoquery)
        phores = mycurser.fetchall()
        with col9:
            uppho = st.text_input('Phone', phores[0][0])
        streetquery = "select street from person where Name='{}'".format(selectname)
        mycurser.execute(streetquery)
        strres = mycurser.fetchall()
        with col11:
            upstr = st.text_input('Street', strres[0][0])
        distquery = "select district from person where Name='{}'".format(selectname)
        mycurser.execute(distquery)
        disres = mycurser.fetchall()
        with col13:
            updis = st.text_input('District', disres[0][0])
        staquery = "select state from person where Name='{}'".format(selectname)
        mycurser.execute(staquery)
        stares = mycurser.fetchall()
        with col15:
            upsta = st.text_input('State', stares[0][0])
        pinquery = "select pincode from person where Name='{}'".format(selectname)
        mycurser.execute(pinquery)
        pinres = mycurser.fetchall()
        with col17:
            uppin = st.text_input('Pincode', pinres[0][0])
        update1,update2,update3=st.columns([2.5,1,2])
        with update2:
            btn=st.button('Update')
        if btn==True:
            upquery="update person set Name='{}',designation='{}',website='{}',mail='{}',phone='{}',street='{}',district='{}',state='{}',pincode='{}' where Name='{}'".format(upname,updes,upweb,upmail,uppho,upstr,updis,upsta,uppin,selectname)
            mycurser.execute(upquery)
            mydb.commit()
            st.write('#')
            sp1,sp2,sp3=st.columns([1.5,1,1.5])
            with sp2:
                with st.spinner('Waiting for Confirmation...'):
                    time.sleep(2)
                    st.success('Update Successfully ! ')
    except:
        st.error('Record is Empty !')

elif selected=='Delete':
    st.markdown('#')
    st.markdown("<h2 style= 'color: white;font-size: 40px;'>Delete the Record</h2>",
                unsafe_allow_html=True)
    del1,del2,del3=st.columns([1,2,1])
    namequery = 'select Name from person'
    namelst = []
    mycurser.execute(namequery)
    nameresult = mycurser.fetchall()
    for i in nameresult:
        namelst.append(i[0])
    with del2:
        st.write('#')
        st.write('')
        selectname = st.selectbox('Choose the Name', namelst)
        st.write('')
        st.write('')
        delbtn=st.button('Delete Record')
        if delbtn==True:
            delete = "delete from person where Name='{}'".format(selectname)
            mycurser.execute(delete)
            mydb.commit()
            st.write('#')
            sp1, sp2, sp3 = st.columns([0.5, 1, 0.5])
            with sp2:
                with st.spinner('Waiting for Confirmation...'):
                    time.sleep(2)
                    st.success('Delete Successfully ! ')


elif selected=='Download':
    st.markdown('#')
    st.markdown("<h2 style= 'color: white;font-size: 40px;'>Download the Record</h2>",
                unsafe_allow_html=True)
    namequery = 'select Name from person'
    namelst = []
    mycurser.execute(namequery)
    nameresult = mycurser.fetchall()
    for i in nameresult:
        namelst.append(i[0])
    c1,c2,c3=st.columns([1,2,1])
    st.write('#')
    with c2:
        st.write('#')
        st.write('')
        selectname = st.selectbox('Choose the Name', namelst)
    dow1,dow2,dow3=st.columns([2,1.8,2])
    def detcsv():
        dic = {'Name': personres[0][0], 'Designation': personres[0][1], 'Website': personres[0][2],
               'Mail': personres[0][3], 'Phone': personres[0][4], 'Street': personres[0][5],
               'District': personres[0][6], 'State': personres[0][7], 'Pincode': personres[0][8]}
        df = pd.DataFrame(dic, index=[0])
        return df
    def detjson():
        dic = {'Name': personres[0][0], 'Designation': personres[0][1], 'Website': personres[0][2],
               'Mail': personres[0][3], 'Phone': personres[0][4], 'Street': personres[0][5],
               'District': personres[0][6], 'State': personres[0][7], 'Pincode': personres[0][8]}
        return dic
    with dow2:
        select=st.selectbox('Choose the Format',['','CSV','JSON'])
        if select=='CSV':
            try:
                sp1, sp2, sp3 = st.columns([1, 2, 1])
                with sp2:
                    st.markdown('#')
                    with st.spinner('Please Wait . . .'):
                        time.sleep(0.5)
                query = 'select * from person where Name=%s'
                mycurser.execute(query, (selectname,))
                personres = mycurser.fetchall()
                df=detcsv()
                def csv(df):
                    return df.to_csv().encode('utf-8')
                downcsv=csv(df)
                csvbtn=st.download_button('Download CSV',downcsv,file_name='{} Data.csv'.format(selectname),mime='csv')
            except:
                st.warning('Record is Empty !')

        elif select=='JSON':
            try:
                sp1, sp2, sp3 = st.columns([1, 2, 1])
                with sp2:
                    st.markdown('#')
                    with st.spinner('Please Wait . . .'):
                        time.sleep(0.5)
                query = 'select * from person where Name=%s'
                mycurser.execute(query, (selectname,))
                personres = mycurser.fetchall()
                dic=detjson()
                js=json.dumps(dic)
                jsonbtn=st.download_button(label='Download JSON',file_name='{} Data.json'.format(selectname),mime='application/json',data=js)
            except:
                st.error('Record is Empty !')

elif selected == "Connect":
    st.header(":red[Linkedin] : https://www.linkedin.com/in/bhadrinath/")
    st.header(":red[Email] : bhadri0121@gmail.com")
    st.header(":red[View More] Projects : [GitHub](https://github.com/bbn21)")

hide_st_style = """
                 <style>
                 #MainMenu {visibility:hidden;}
                 footer {visibility:hidden;}

                 </style>"""
st.markdown(hide_st_style, unsafe_allow_html=True)