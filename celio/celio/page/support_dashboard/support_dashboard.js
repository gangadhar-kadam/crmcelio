frappe.require('assets/js/chart.js');
frappe.pages['support-dashboard'].onload = function(wrapper) { 
	frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Dashbaord',
		single_column: true
	});
$(' <div id="salesmain" style="height:10%; width:100%;" >\
	<table class="table table-bordered" style="height:20px; width:100%;border-radius:10px;background-color: #f9f9f9;">\
	<tr width="100%">\
	<td width="50%"><div class="browcl" id ="brow"  style="min-height: 50px;"><b></div></td>\
	<td width="50%"><div class="crowcl" id ="crow"  style="min-height: 50px;"><b></div></td>\
	</tr>\
	</table>\
	<div id="head" style="height:100%; width:100%;"><b>Branch-wise Support Tickets</tr></table></div><div id="salesmain" style="height:100%; width:100%;" >\
	<table class="table table-bordered" style="height:200px; width:100%;border-radius:10px;background-color: #f9f9f9;">\
	<tr width="100%">\
	<td width="100%"><div class="grossrowcl" id ="grossrow"  style="min-height: 50px;"></div></td>\
	</tr>\
	</table>\
	<div id="head" style="height:100%; width:100%;"><b>Pending Support Tickets Summary</tr></table></div><div id="salesmain" style="height:100%; width:100%;" >\
	<table class="table table-bordered" style="height:200px; width:100%;border-radius:10px;background-color: #f9f9f9;">\
	<tr width="100%">\
	<td width="100%"><div class="arowcl" id ="arow"  style="min-height: 50px;"></div></td>\
	</tr>\
	</div>\
	</table>').appendTo($(wrapper).find('.layout-main'));

	new frappe.Dashboard(wrapper);

}	

frappe.Dashboard = Class.extend({
	init: function(wrapper) {
		this.wrapper = wrapper;
		this.body = $(this.wrapper).find(".layout-main");
		this.open_closed_sp();
		this.pending_sp();
		this.support_list();
		this.support_report();
		},

	open_closed_sp:function(){
			// console.log(user);
			var me = this;			
		    frappe.call({
			method:"celio.celio.page.support_dashboard.support_dashboard.get_supp_tkt",
			args:{'user':user},
			callback: function(r) {
			console.log(r.message);
			var options = {packages: ['corechart'], callback : drawChart};
		    google.load('visualization', '1', options);
		    function drawChart() {
		  	mydata=[['Channel', 'Open Tickets', 'Closed Tickets']];
		  	 for(var x in r.message.supp_tckt){
  				mydata.push(r.message.supp_tckt[x]);
               }
            var data = google.visualization.arrayToDataTable(mydata);
		    var options = {
		      hAxis: {title: 'No of Tickets',titleTextStyle: {color: '#009933'}},
		      vAxis: {title: 'Department',minValue:0,titleTextStyle: {color: '#009933'}},
		      width: 920,
        	  height:300,
        	  legend: { position: 'top', maxLines: 3 },
        	  isStacked: true        	 
		    };
		    $(me.wrapper).find('.grossrowcl').empty();
		    var chart = new google.visualization.BarChart(document.getElementById("grossrow"));
		    chart.draw(data, options);
		    }
		    }
	    });
	},

	pending_sp:function(){
			console.log("in make grosss");
			var me = this;			
		    frappe.call({
			method:"celio.celio.page.support_dashboard.support_dashboard.get_pending_sp",
			args:{'user':user},
			callback: function(r) {
			console.log(r.message);
			var options = {packages: ['corechart'], callback : drawChart};
		    google.load('visualization', '1', options);
		    function drawChart() {
		  	mydata=[['Tickets','Pending Tickets(In days)']];
		  	 for(var x in r.message.pending_sp){
  				mydata.push(r.message.pending_sp[x]);
               }
            var data = google.visualization.arrayToDataTable(mydata);
		    var options = {
		      hAxis: {title: 'No.of pending tickets',titleTextStyle: {color: '#009933'}},
		      vAxis: {title: 'User',minValue:0,titleTextStyle: {color: '#009933'}},
		      width: 920,
        	  height:350,
        	  legend: { position: 'top', maxLines: 3 }
		    };
		    $(me.wrapper).find('.arowcl').empty();
		    var chart = new google.visualization.BarChart(document.getElementById("arow"));
		    chart.draw(data, options);
		    }
		    }
	    });
	},

	support_list:function(){
			var me = this;
			$("#brow").html('<a href="../desk#List/Support Ticket">Support Ticket List</a>')
	},

	support_report:function(){
			var me = this;
			$("#crow").html('<a href="../desk#Report/Support Ticket">Support Ticket Report</a>')
	},

	});