// ==UserScript==
// @name         Color Cosmetics
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  try to take over the world!
// @author       You
// @match        http*://ftba.nmpa.gov.cn:8181/ftban/fw.jsp
// @grant        none
// @require      https://unpkg.com/ajax-hook@2.0.3/dist/ajaxhook.min.js
// @require      https://code.jquery.com/jquery-3.6.0.min.js
// ==/UserScript==

let baseURL = 'http://ftba.nmpa.gov.cn:8181/ftban/'

ah.proxy({
    //请求发起前进入
    onRequest: (config, handler) => {
        // console.log(config.url)
        if (config.body != null) {
            if (config.body.substr(0,2) == 'on'){
                let res_body = config.body
                let cur_page = res_body.split('&')[res_body.split('&').length-1]
                console.log(cur_page, 'begin')
            }
        }
        handler.next(config);
    },
    //请求发生错误时进入，比如超时；注意，不包括http状态码错误，如404仍然会认为请求成功
    onError: (err, handler) => {
        console.log(err.type)
        handler.next(err)
    },
    //请求成功后进入
    onResponse: (response, handler) => {
        if (response.config.body != null) {
            if (response.config.body.substr(0,2) == 'on'){
                let res_body = response.config.body
                let cur_page = res_body.split('&')[res_body.split('&').length-1]

                console.log(cur_page, 'doing')
            }

            let result = JSON.parse(response.response)
            let company_list = result.list

            var dict_records = []

            for (let item in company_list) {
                let cur_line = company_list[item]
                let off = item.is_off =="Y" ? "（已注销）":"";
                let cur_applySn = cur_line.applySn + "" + off
                let cur_url = baseURL + "itownet/hzp_ba/fw/pz.jsp?processid=" + cur_line.processid + "&nid=" + cur_line.newProcessid
                let cur_enterpriseName = cur_line.enterpriseName+"（" + cur_line.apply_enter_address+"）"
                // console.log(cur_url, cur_applySn, cur_enterpriseName, cur_line.newProcessid, cur_line.productName, cur_line.provinceConfirm, cur_line.apply_enter_address)
                //发送到dis_pharma_website的数据库中

                dict_records.push({'applySn': cur_applySn, 'url': cur_url, 'enterpriseName': cur_enterpriseName, 'date': cur_line.provinceConfirm, 'productname': cur_line.productName});
                // $.ajax({
                //     type: 'POST',
                //     url: "http://127.0.0.1:5000/postDummydata",
                //     data: {'applySn': cur_applySn, 'url': cur_url, 'enterpriseName': cur_enterpriseName, 'date': cur_line.provinceConfirm, 'productname': cur_line.productName},
                //     success: function(res) {
                //         // console.log('done');
                //     }
                // });
            }
            if (dict_records.length > 0) {
                $.ajax({
                    type: 'POST',
                    url: "http://127.0.0.1:5000/postDummydata",
                    data: {'records': dict_records},
                    success: function(res) {
                        // console.log('done');
                    }
                });
            }
            handler.next(response)
        }
    }
})
