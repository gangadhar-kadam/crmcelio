import frappe

@frappe.whitelist()
def get_escalation_for_supportticket():
  from frappe.utils import cstr
  from frappe.utils.email_lib import sendmail
  # frappe.errprint("Hii")
  # print "Hello"
  # msg="support ticket creation"
  # sendmail('priya.s@indictranstech.com', subject="Create Supp.Ticket", msg=msg)
  
  j = 0       
  from frappe.utils import get_first_day, get_last_day, add_to_date, nowdate, getdate
  #qry1="select name from `tabSupport Ticket` t where t.status='Open' and t.creation < DATE_SUB(NOW(), INTERVAL 24+"+cstr(j)+" HOUR) AND  t.creation > DATE_SUB(NOW(), INTERVAL 48+"+cstr(j)+" HOUR)"
  qry=frappe.db.sql("select name from `tabSupport Ticket` t where t.status='Open' and t.creation < DATE_SUB(NOW(), INTERVAL 24+"+cstr(j)+" HOUR) AND  t.creation > DATE_SUB(NOW(), INTERVAL 48+ '%s' HOUR)",(j),as_list=1)
  frappe.errprint("in 24 "+cstr(qry))
  
  if qry:
    for [st] in qry:
      region=frappe.db.sql("select territory from `tabSupport Ticket` where name=%s",(st),as_list=1)
      regional_head=frappe.db.sql("select parent from `tabDefaultValue` where  defkey = '%s' and defvalue = '%s'"%('territory',region[0][0]))
      frappe.errprint(region[0][0])
      sup_tkt=frappe.db.sql("update `tabSupport Ticket` set assigned_to='%s' where name='%s'"%(regional_head[0][0],st),as_list=1)
      frappe.db.commit()
      flg=frappe.db.sql("select flag from `tabSupport Ticket` where name=%s",(st),as_list=1)
      # frappe.errprint(flg[0][0])
      if flg[0][0]=='not' and len(regional_head[0]) > 0:
        msg=frappe.db.sql("select template from `tabEmail Template` where template_type='Escalation'",as_list=1)
        sendmail(regional_head[0][0], subject="Support Ticket Escalation", msg = msg[0][0])
        flg1=frappe.db.sql("update `tabSupport Ticket` set flag='fst' where name=%s",(st),as_list=1)
        frappe.db.commit()

  qr=frappe.db.sql("select name from `tabSupport Ticket` t where t.status='Open' and  t.creation < DATE_SUB(NOW(), INTERVAL 48+"+cstr(j)+" HOUR) AND t.creation > DATE_SUB(NOW(), INTERVAL 100+ '%s' HOUR)",(j),as_list=1)
  frappe.errprint("in 48 "+cstr(qr))
  if qr:
    for [st1] in qr:
      frappe.errprint(st1)
      # supp_manager=frappe.db.sql("select parent from `tabDefaultValue` where  defkey = '%s' and defvalue = 'Support Manager'"%('role'))
      supp_manager=frappe.db.sql("select parent from `tabUserRole` where role='Support Manager' and parent!='Administrator'")
      frappe.errprint(supp_manager[0][0])
      sup_tkt1=frappe.db.sql("update `tabSupport Ticket` set assigned_to='%s' where name='%s'"%(supp_manager[0][0],st1),as_list=1)
      frappe.db.commit()
      flg1=frappe.db.sql("select flag from `tabSupport Ticket` where name=%s",(st1),as_list=1)
      # frappe.errprint(flg1[0][0])
      if flg1[0][0]=='fst':
        msg=frappe.db.sql("select template from `tabEmail Template` where template_type='Escalation'",as_list=1)
        sendmail(supp_manager[0][0], subject="Support Ticket Escalation", msg = msg[0][0])
        f=frappe.db.sql("update `tabSupport Ticket` set flag='snd' where name=%s",(st1),as_list=1)
        frappe.db.commit()


@frappe.whitelist()
def get_supp_tkt(user):
  frappe.errprint("on dashboard")
  role=frappe.db.sql("select name from `tabRole`", as_list=1)
  for [r] in role:
    rl=frappe.db.sql("select role from `tabUserRole` where parent=%s",(user),as_list=1)
    # frappe.errprint(rl[0][0])
    if rl[0][0]=='Helpdesk User':
      supp_tckt=frappe.db.sql("""select priority,sum(case when status='Open' then _count else 0 end) 
        as open_count,sum(case when status='Closed' then _count else 0 end) as close_count 
        from (select priority,status,count(*) as _count from `tabSupport Ticket` 
        where creation > DATE_SUB(CURDATE(), INTERVAL 1 DAY) group by  priority,status)foo 
        group by priority""",as_list=1)
      ret={'supp_tckt' : supp_tckt}
      return ret

    elif rl[0][0]=='Support User':
      supp_tckt=frappe.db.sql("""select priority,sum(case when status='Open' then _count else 0 end) 
        as open_count,sum(case when status='Closed' then _count else 0 end) as close_count 
        from (select priority,status,count(*) as _count from `tabSupport Ticket` 
        where creation > DATE_SUB(CURDATE(), INTERVAL 1 DAY) group by  priority,status)foo 
        group by priority""",as_list=1)
      ret={'supp_tckt' : supp_tckt}
      return ret

    elif rl[0][0]=='Support Regional Head':
      supp_tckt=frappe.db.sql("""select name,(select count(*) from `tabSupport Ticket` where 
          status='Open' and creation > DATE_SUB(CURDATE(), INTERVAL 1 DAY) and branch_id=b.name) 
          as Open_Count, (select count(*) from `tabSupport Ticket` where status='Closed' and 
          creation > DATE_SUB(CURDATE(), INTERVAL 1 DAY) and branch_id=b.name) as Close_Count
          from `tabCelio Department` b""",as_list=1)
      ret={'supp_tckt' : supp_tckt}
      return ret

    elif rl[0][0]=='Support Manager':
      # frappe.errprint("rl")
      supp_tckt=frappe.db.sql("""select territory,(select count(*) from `tabSupport Ticket` where 
        status='Open' and creation > DATE_SUB(CURDATE(), INTERVAL 1 DAY) and territory=b.territory) 
        as Open_Count, (select count(*) from `tabSupport Ticket` where status='Closed' and 
        creation > DATE_SUB(CURDATE(), INTERVAL 1 DAY) and territory=b.territory) as Close_Count
        from `tabCelio Department` b""",as_list=1)
      ret={'supp_tckt' : supp_tckt}
      return ret


@frappe.whitelist()
def get_pending_sp(user):
  role=frappe.db.sql("select name from `tabRole`", as_list=1)
  for [r] in role:
    rl=frappe.db.sql("select role from `tabUserRole` where parent=%s",(user),as_list=1)
    branch=frappe.db.sql("select distinct defvalue from `tabDefaultValue` where defkey='celio department' and parent=%s",(user),as_list=1)
    territory=frappe.db.sql("select distinct defvalue from `tabDefaultValue` where defkey='territory' and parent=%s",(user),as_list=1)
    frappe.errprint(branch)
    if rl[0][0]=='Helpdesk User':
      pending_sp=frappe.db.sql("""select assigned_to,count(name) from `tabSupport Ticket` where 
         creation < DATE_SUB(CURDATE(), INTERVAL 1 DAY) and status <>'Closed' and branch_id=%s group by assigned_to""",(branch[0][0]),as_list=1)
      ret={'pending_sp' : pending_sp}
      return ret

    elif rl[0][0]=='Support User':
      pending_sp=frappe.db.sql("""select assigned_to,count(name) from `tabSupport Ticket` where 
         creation < DATE_SUB(CURDATE(), INTERVAL 1 DAY) and status <>'Closed' and branch_id=%s group by assigned_to""",(branch[0][0]),as_list=1)
      ret={'pending_sp' : pending_sp}
      return ret

    elif rl[0][0]=='Support Regional Head':
      pending_sp=frappe.db.sql("""select assigned_to,count(name) from `tabSupport Ticket` where 
         creation < DATE_SUB(CURDATE(), INTERVAL 1 DAY) and status <>'Closed' and territory=%s group by assigned_to""",(territory[0][0]),as_list=1)
      ret={'pending_sp' : pending_sp}
      return ret

    elif rl[0][0]=='Support Manager':
      pending_sp=frappe.db.sql("""select territory,count(name) from `tabSupport Ticket` where 
         creation < DATE_SUB(CURDATE(), INTERVAL 1 DAY) and status <>'Closed' group by territory""",as_list=1)
      ret={'pending_sp' : pending_sp}
      return ret



