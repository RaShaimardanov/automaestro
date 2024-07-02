#
cmd-start = Привет, { $user }!
main-menu-user = Вы находитесь в главном меню.
    Выберите действие:
register-car-scene-enter = Введите государственный номер Вашего автомобиля в формате <b>Н525ММ198</b>
input-data-invalid = Пожалуйста,  проверьте корректность введенных данных.
input-license-plate-number-used =
    Гос. номер <b>{ $data }</b> используется другим пользователем.
    { input-data-invalid }
input-license-plate-number-success = Данные сохранены.
# Сцена профиля
profile-menu-scene-enter =
    Ваши данные: { $user }
    Гос. номер автомобиля: <b>{ $license_plate_number }</b>

poll-scene-leave = Благодарим Вас за участие в исследовании!
receive-notification-ask = Уведомления <b>{ $position ->
                                              [1] включены
                                              *[other] откючены
                                           }</b>.
    Хотите получить уведомление по готовности Вашего автомобиля?
offer-receive-notifications = Так же у Вас есть возможность <b>получить уведомления о готовности вашего автомобиля</b>.
    Пожалуйста, выберите, хотите ли вы получить уведомление, используя кнопки ниже.
