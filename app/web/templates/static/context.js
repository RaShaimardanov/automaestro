    let tg = window.Telegram.WebApp;
    if(tg !== undefined) {
        tg.ready()
        tg.expand();  //  открываем окно во весь экран
        tg.enableVerticalSwipes() //  подключаем вертикальную прокрутку
        function setupBackButton() {
            //  устанавливаем кнопку < Назад
            const currentUrl = window.location.pathname;
            if (currentUrl !== '/admin/') {
                tg.BackButton.show();
            }
            else {
                tg.BackButton.hide()
            }
        }
        setupBackButton();

        function manageBackButton() {
            //  обрабатываем нажатие кнопки < Назад
            const currentUrl = window.location.pathname;
            if (currentUrl === '/admin/') {
                tg.close();
            } else {
                history.back();
            }
        }
        tg.onEvent('backButtonClicked', manageBackButton)

        if (tg.WebApp !== undefined && tg.WebApp.initData !== undefined) {
            let user_telegram_id = tg.initDataUnsafe.user.id
            document.cookie = "telegram_id=" + user_telegram_id + "; max-age=2592000; path=/";
        }    // добавляем telegram_id в куки
    }
    function showhide(d) {
        // функция показать/скрыть div
        d.style.display = (d.style.display !== "none") ? "none" : "block";
        d.scrollIntoView({behavior:'smooth', block:'start'});
    }