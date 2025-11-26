"""
Dashboard routes - statistics, charts, and PDF export
"""
from flask import Blueprint ,render_template ,jsonify ,send_file 
from flask_login import login_required ,current_user 
from database import get_db_connection 
from datetime import datetime ,timedelta 
from collections import defaultdict 


dashboard_bp =Blueprint ('dashboard',__name__ )

@dashboard_bp .route ('/dashboard')
@login_required 
def dashboard ():
    """Render dashboard page"""
    return render_template ('dashboard.html',user =current_user )

@dashboard_bp .route ('/profile')
@login_required 
def profile ():
    """Render profile page"""
    return render_template ('profile.html',user =current_user )

@dashboard_bp .route ('/api/dashboard/stats')
@login_required 
def get_stats ():
    """Get dashboard statistics"""
    conn =get_db_connection ()


    expenses =conn .execute (
    'SELECT * FROM expenses WHERE user_id = ?',
    (current_user .id ,)
    ).fetchall ()


    total_spending =sum (exp ['amount']for exp in expenses )


    current_month =datetime .now ().strftime ('%Y-%m')
    monthly_spending =sum (
    exp ['amount']for exp in expenses 
    if exp ['date'].startswith (current_month )
    )


    today =datetime .now ().strftime ('%Y-%m-%d')
    today_spending =sum (
    exp ['amount']for exp in expenses 
    if exp ['date']==today 
    )


    category_totals =defaultdict (float )
    for exp in expenses :
        category_totals [exp ['category']]+=exp ['amount']


    monthly_data =defaultdict (float )
    for exp in expenses :
        month =exp ['date'][:7 ]
        monthly_data [month ]+=exp ['amount']


    sorted_months =sorted (monthly_data .keys (),reverse =True )[:6 ]
    sorted_months .reverse ()

    chart_data ={
    'labels':sorted_months ,
    'data':[monthly_data [month ]for month in sorted_months ]
    }

    conn .close ()

    return jsonify ({
    'total_spending':total_spending ,
    'monthly_spending':monthly_spending ,
    'today_spending':today_spending ,
    'category_totals':dict (category_totals ),
    'chart_data':chart_data 
    })

@dashboard_bp .route ('/api/export/pdf')
@login_required 
def export_pdf ():
    """Export expenses as PDF"""
    from reportlab .lib .pagesizes import letter 
    from reportlab .lib import colors 
    from reportlab .lib .styles import getSampleStyleSheet 
    from reportlab .platypus import SimpleDocTemplate ,Table ,TableStyle ,Paragraph ,Spacer 
    from io import BytesIO 

    conn =get_db_connection ()


    current_month =datetime .now ().strftime ('%Y-%m')
    expenses =conn .execute (
    'SELECT * FROM expenses WHERE user_id = ? AND date LIKE ? ORDER BY date DESC',
    (current_user .id ,f'{current_month }%')
    ).fetchall ()
    conn .close ()


    buffer =BytesIO ()
    doc =SimpleDocTemplate (buffer ,pagesize =letter )
    elements =[]
    styles =getSampleStyleSheet ()


    title =Paragraph (f"<b>Expense Report - {datetime .now ().strftime ('%B %Y')}</b>",styles ['Title'])
    elements .append (title )
    elements .append (Spacer (1 ,12 ))


    user_info =Paragraph (f"<b>Name:</b> {current_user .name }<br/><b>Email:</b> {current_user .email }",styles ['Normal'])
    elements .append (user_info )
    elements .append (Spacer (1 ,12 ))


    data =[['Date','Title','Category','Amount']]
    total =0 

    for exp in expenses :
        data .append ([
        exp ['date'],
        exp ['title'],
        exp ['category'],
        f"{current_user .currency }{exp ['amount']:.2f}"
        ])
        total +=exp ['amount']

    data .append (['','','Total:',f"{current_user .currency }{total :.2f}"])

    table =Table (data )
    table .setStyle (TableStyle ([
    ('BACKGROUND',(0 ,0 ),(-1 ,0 ),colors .grey ),
    ('TEXTCOLOR',(0 ,0 ),(-1 ,0 ),colors .whitesmoke ),
    ('ALIGN',(0 ,0 ),(-1 ,-1 ),'CENTER'),
    ('FONTNAME',(0 ,0 ),(-1 ,0 ),'Helvetica-Bold'),
    ('FONTSIZE',(0 ,0 ),(-1 ,0 ),12 ),
    ('BOTTOMPADDING',(0 ,0 ),(-1 ,0 ),12 ),
    ('BACKGROUND',(0 ,-1 ),(-1 ,-1 ),colors .beige ),
    ('GRID',(0 ,0 ),(-1 ,-1 ),1 ,colors .black )
    ]))

    elements .append (table )
    doc .build (elements )

    buffer .seek (0 )
    return send_file (
    buffer ,
    as_attachment =True ,
    download_name =f'expense_report_{datetime .now ().strftime ("%Y-%m")}.pdf',
    mimetype ='application/pdf'
    )