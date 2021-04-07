// ==UserScript==
// @name         Color Cosmetics Detail
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  try to take over the world!
// @author       You
// @match        http*://ftba.nmpa.gov.cn:8181/ftban/itownet/hzp_ba/fw/pz.jsp*
// @grant        none
// @require      https://unpkg.com/ajax-hook@2.0.3/dist/ajaxhook.min.js
// @require      https://code.jquery.com/jquery-3.6.0.min.js
// @run-at       document-start
// ==/UserScript==

let baseURL = 'http://ftba.nmpa.gov.cn:8181/ftban/'

ah.proxy({
    //请求发起前进入
    onRequest: (config, handler) => {
        handler.next(config);
    },
    //请求发生错误时进入，比如超时；注意，不包括http状态码错误，如404仍然会认为请求成功
    onError: (err, handler) => {
        console.log(err.type)
        handler.next(err)
    },
    //请求成功后进入
    onResponse: (response, handler) => {
        let result = JSON.parse(response.response)
        if (result.actual_enter_address != undefined) {
            var cas=0;//配方编号
    		var ylid=1;//成分编号
    		var khFlag=true;
    		var cnames=new Array();
    		var pfObj=new Object();
            var pfObjonly = "";
    		jQuery.each(result.pfList,function(i,item){
    			cas=item.pfname;//得到配方名称
                pfObjonly = pfObjonly + item.cname + ';'
    			if(pfObj[cas]==undefined){
    				pfObj[cas]=new Array();
    				cnames.push(cas);
    			}
    			if(ylid==1){
    				pfObj[cas].push(item.cname)
    			}else{
    				if(ylid==item.ylid){
        				var lastObj=pfObj[cas].pop();
        				lastObj=lastObj.replace(")","");
        				lastObj=lastObj.replace("(","");
        				lastObj="("+lastObj+","+item.cname+")";
        				pfObj[cas].push(lastObj);
        			}else{
        				pfObj[cas].push(item.cname)
        			}
    			}
    			ylid=item.ylid
    		})
            var pfStr='';
            var sjqy=new Array();
    		jQuery.each(pfObj,function(i,item){
    			var str = JSON.stringify(item);
    			pfStr+=i+":"+str+"<br>";
    		});
            //生产企业
            jQuery.each(result.sjscqyList,function(i,item){
    			sjqy.push(item.enterprise_name);
    		});
            //判断是否注销产品
            var off = result.is_off =="Y" ? "（"+result.applyDateE+"已注销）":""
            alert(result.productname + pfObjonly.substr(0, pfObjonly.length-1) + result.scqyUnitinfo.enterprise_name + JSON.stringify(sjqy) + off)
            // console.log(result.productname + pfObjonly.substr(0, pfObjonly.length-1), result.scqyUnitinfo.enterprise_name + JSON.stringify(sjqy) + off)
            //发送数据到数据库
            $.ajax({
                type: 'POST',
                url: "http://127.0.0.1:5000/postIngredientdata",
                data: {'productname': result.productname, 'processid': response.config.body.substr(10), 'ingredients_lt': pfObjonly.substr(0, pfObjonly.length-1), 'brandowner': result.scqyUnitinfo.enterprise_name, 'manufactures': JSON.stringify(sjqy), 'cancellation':off},
                success: function(res) {
                    // console.log('done');
                }
            });
        }
        handler.next(response)
    }
})
