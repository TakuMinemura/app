window.addEventListener("load" , function (){

    let config_dt = {
        dateFormat: "Y-m-d",
        locale: "ja"
    }

    //flatpickrのCDNによりflatpickr関数が使える。第一引数はflatpickrを反映させる要素、第二引数は設定
    flatpickr(".dt", config_dt);

});
