// ==UserScript==
// @name         Qi Cha Cha
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  try to take over the world!
// @author       You
// @match        https://www.qcc.com/firm/*
// @icon         https://www.google.com/s2/favicons?domain=qcc.com
// @grant        none
// @run-at       document-end
// @require      https://code.jquery.com/jquery-3.6.0.min.js
// ==/UserScript==

(function() {
    'use strict';

    var dic_data = new Object()

    let company_name = $('div.row.title.jk-tip h1').text()
    var lt_tags = new Array()
    jQuery.each($('div.row.tags span') ,function(i,item){
        if (item.innerText.length>0 && item.innerText.indexOf('自身')<0 && item.innerText.indexOf('司法')<0) {
            lt_tags.push(item.innerText)
        }
    })
    let company_tags = $('div.row.tags span').text()
    let phone = $('span.phone-status').next().text()
    var email = ""
    jQuery.each($('span.fc a.text-primary').text().split(' '), function(i, item){
        if (item.indexOf('@')>0) {email = item}
    })
    var lt_gtabs = new Array()
    jQuery.each($('div.row.gtag a') ,function(i,item){
        lt_gtabs.push(item.innerText)
    })
    let company_intro = encodeURI($('span.cvlu.introExpand').text().replace('收起',''))

    dic_data['公司名称'] = company_name
    dic_data['企查查快捷'] = lt_tags
    dic_data['电话'] = phone
    dic_data['邮箱'] = email
    dic_data['标签'] = lt_gtabs
    dic_data['简介'] = company_intro

    jQuery.each($('td.tb'), function(i, item){
        dic_data[$.trim($(item).text())]=$.trim($(item).next().text())
        // console.log($.trim($(item).text()), $.trim($(item).next().text()))
    })

    $.ajax({
        type: 'POST',
        url: "http://127.0.0.1:5000/insertqichacha",
        data: JSON.stringify(dic_data),
        success: function(res) {
            alert('done')
        }
    });


})();
