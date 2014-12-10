import frappe

@frappe.whitelist()
def get_escalation_for_supportticket():
  from frappe.utils import cstr
  from frappe.utils.email_lib import sendmail
  frappe.errprint("Hii")
  # print "hiii"
   #      aa="select distinct(subdate(CURDATE(), 1)) from `tabHoliday` where subdate(CURDATE(), 1) not in (select holiday_date from `tabHoliday` where parent='2014-2015/Maharashtra/001')"
   #      res=frappe.db.sql(aa)
   #      j=0
   #      if res:
   #             for i in range (2,15):
			# bb="select distinct(subdate(CURDATE(), "+cstr(i)+")) from `tabHoliday`"
   #                      #print bb
			# res1=frappe.db.sql(bb)
			# if res1:
			#   cc="select distinct(subdate(CURDATE(), 1)) from `tabHoliday` where '"+cstr(res1[0][0])+"' in (select holiday_date from `tabHoliday` where parent='2014-2015/Maharashtra/001')"
			#   #print cc
			#   res2=frappe.db.sql(cc)
			#   if res2:
   #    			      j=j+24
			#   else:
   #                           print "breaning"
			#      break
  j = 0       
  from frappe.utils import get_first_day, get_last_day, add_to_date, nowdate, getdate
  #qry1="select name from `tabSupport Ticket` t where t.status='Open' and t.creation < DATE_SUB(NOW(), INTERVAL 24+"+cstr(j)+" HOUR) AND  t.creation > DATE_SUB(NOW(), INTERVAL 48+"+cstr(j)+" HOUR)"
  qry=frappe.db.sql("select name from `tabSupport Ticket` t where t.status='Open' and t.creation < DATE_SUB(NOW(), INTERVAL 24+"+cstr(j)+" HOUR) AND  t.creation > DATE_SUB(NOW(), INTERVAL 48+ '%s' HOUR)",(j),as_list=1)
  frappe.errprint("in 24 "+cstr(qry))
  msg="Hello, Support ticket '"+cstr(qry)+"' is assigned to you.."
  sendmail('priya.s@indictranstech.com', subject="Support Ticket Escalation", msg = msg)
  if qry:
    for [k] in qry:
      frappe.errprint(k)
      p=frappe.db.sql("select territory from `tabSupport Ticket` where name=%s",(k),as_list=1)
      frappe.errprint(p)
      w=frappe.db.sql("select parent from `tabDefaultValue` where  defkey = '%s' and defvalue = '%s'"%('territory',p[0][0]))
      frappe.errprint(w[0][0])
      ee="update `tabSupport Ticket` set assigned_to='"+cstr(w[0][0])+"' where name='"+cstr(k)+"'"
      frappe.db.sql(ee)
      frappe.db.commit()
      frappe.errprint("Updated")

  qr=frappe.db.sql("select name from `tabSupport Ticket` t where t.status='Open' and  t.creation < DATE_SUB(NOW(), INTERVAL 48+"+cstr(j)+" HOUR) AND t.creation > DATE_SUB(NOW(), INTERVAL 72+ '%s' HOUR)",(j),as_list=1)
  frappe.errprint("in 48 "+cstr(qr))
  if qr:
    for [l] in qr:
      frappe.errprint(l)
      q=frappe.db.sql("Select p.name from `tabProfile` p, `tabUserRole` r where r.role='Support Manager' and r.parent=p.name")
      ff="update `tabSupport Ticket` set assigned_to_higher_level='"+cstr(q[0][0])+"' where name='"+cstr(l)+"'"
      frappe.db.sql(ff)
      frappe.db.commit()
      sendmail('priya.s@indictranstech.com', subject="Support Ticket Escalation", msg = msg)
      frappe.errprint("Updated")
