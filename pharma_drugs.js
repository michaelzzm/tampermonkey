// ==UserScript==
// @name         Medical NMPA
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  try to take over the world!
// @author       You
// @match        http*://app1.nmpa.gov.cn/*
// @grant        none
// @require      https://unpkg.com/ajax-hook@2.0.3/dist/ajaxhook.min.js
// @require      https://code.jquery.com/jquery-3.6.0.min.js
// ==/UserScript==

var cnt_page
var pagelasttime
var cur_drug
var lt_drugs

(function() {
    'use strict'

    lt_drugs = ['Pantoprazole Sodium']

    for(var drug in lt_drugs) {
        console.log(lt_drugs[drug])
        cur_drug = lt_drugs[drug]
        $('#keyword').val(lt_drugs[drug])
        setTimeout(() => keywordSubmit(), 5000)
    }

//     $('#keyword').val('Lidocaine')
//     keywordSubmit()

//     var interval = null
//     var startPage = 1
//     interval = setInterval(function () {
//         // parseResponse() // 获取响应并且发出到Redis
//         // // 检测是否需要翻页
//         // if (startPage <= endPage){
//         //     devPage(startPage++) // 翻页
//         // }
//         // else {
//         //     clearInterval(interval) // 结束
//         // }
//         if ($('#content form').length > 1) {
//             var str_page = $('#content form').first().attr('action').substr(18)
//             cnt_page = parseInt(str_page.substr(0, str_page.length-1))
//             pagelasttime = 1
//             console.log(cnt_page)
//             clearInterval(interval)
//         }
//     }, 500)

})()

ah.proxy({
    //请求发起前进入
    onRequest: (config, handler) => {
        console.log(config.url)
        handler.next(config);
    },
    //请求发生错误时进入，比如超时；注意，不包括http状态码错误，如404仍然会认为请求成功
    onError: (err, handler) => {
        console.log(err.type)
        handler.next(err)
    },
    //请求成功后进入
    onResponse: (response, handler) => {
        if (response.status == 502) {
            handler.next(response)
            $('#keyword').val(cur_drug)
            keywordSubmit()
            setTimeout(() => devPage(pagelasttime + 1), 8000)
        }
        else {
            // console.log(response.response)
            let paras = response.config.body.split('&')
            var cur_page
            for(var i=0;i<paras.length;i++) {
                if (paras[i].indexOf('curstart=')==0) {
                    cur_page = parseInt(paras[i].substr(9))
                }
            }
            var list = $($.parseHTML(response.response)).find('tr td a')
            for(var j=0;j<list.length;j++) {
                console.log(list[j])
                //发送到pharma_website的数据库中
            }
            if (cur_page == undefined && cnt_page == undefined) {
                var str_page = $($.parseHTML(response.response)).find('form').first().attr('action').substr(18)
                cnt_page = parseInt(str_page.substr(0, str_page.length-1))
                cur_page = 1
                console.log(cnt_page)
            }
            handler.next(response)
            //当发生502时候第一次
            if (cur_page == undefined) {}
            else {
                if (cur_page < cnt_page) {
                    pagelasttime = cur_page
                    setTimeout(() => devPage(cur_page + 1), 8000)
                } else {
                    cnt_page = null
                    console.log('done')
                }
            }
        }
    }
})
