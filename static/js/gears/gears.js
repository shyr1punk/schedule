/**
 * @version 0.1
 * User: Alexey Tarasenko
 * Date: 20.08.13
 * Time: 14:06
 */

/*global $, setInterval, console, localStorage*/
"use strict";
/**
 * Объект Интерфейса, содержащий свойства и методы работы с внешним видом приложения
 * @class
 */
var Interface = {
    /**
     * прокручивает расписание к якорю
     * @function
     * @param {string} aid название якоря, например Monday
     */
    scrollToAnchor: function (aid) {
        var aTag = $("a[name='" + aid + "']");
        $('html,body').animate({scrollTop: aTag.offset().top - 60}, 'slow');
    }
};

/**
 * Конструктор нового объекта-ячейки с расписанием (одна пара одного дня)
 * @param {object} args объект
 * @param {string} [args.daycode=1] порядковый номер дня недели
 * @param {string} [args.dayname=Понедельник] название дня недели
 * @param {string} [args.date=01.01] дата без указания года
 * @param {number} [args.lessonnumber=1] номер пары
 * @param {string} [args.lessontitle='История авиации'] название пары
 * @param {string} [args.teachername='ст. преп. Иванов И.И.] фио препода
 * @param {string} [args.classroom='10р'] название аудитории
 * @param {string} [args.type='lec'] тип пары (лекция, практика, лаба)
 * @constructor
 */
function ScheduleCell(args) {
    this.daycode = args.daycode || '1';
    this.dayname = args.dayname || 'Понедельник';
    this.date = args.date || '01.01';
    this.lessonnumber = args.lessonnumber || 1;
    this.lessontitle = args.lessontitle || 'История авиации';
    this.teachername = args.teachername || 'ст. преп. Иванов';
    this.classroom = args.classroom || '10р';
    this.type = args.type || 'lec';
}
/**
 * Объект Таблица
 */
var Table = {
    /**
     * Массив дней недели для сохранения ячеек расписания типа ScheduleCell
     */
    days: [
        {Monday:    []},
        {Tuesday:   []},
        {Wednesday: []},
        {Thursday:  []},
        {Friday:    []},
        {Saturday:  []},
        {Sunday:    []}],

    /**
     * массив объектов-ячеек(занятий)
     * @property
     */
    LessonsArray: [],

    /**
     * Сортировка выбранных пар по дням (ПН-СБ) и очередности (1-6)
     * Сохраняем в выбранный день недели и выбранную пару информацию
     * Например в (days) понедельник (cell.daycode) третьей парой (cell.lessonnumber) Программирование, лекция, аудитория, преподаватель
     * @param {object} cell ячейка таблицы типа ScheduleCell
     */
    separateDay: function (cell) {
        this.days[cell.daycode[cell.lessonnumber]] = cell;
    },

    /**
     * читает все пары в массив и сортирует по дням и очередности
     */
    getData: function () {
        var self = this;
        $.getJSON('js/json/data.json', function (data) {
            $.each(data, function (key, val) {
                self.LessonsArray[key] = new ScheduleCell({
                    daycode:        val.daycode,
                    dayname:        val.dayname,
                    date:           val.date,
                    lessonnumber:   val.lessonnumber,
                    lessontitle:    val.lessontitle,
                    teachername:    val.teachername,
                    classroom:      val.classroom,
                    type:           val.type
                });
                self.separateDay(self.LessonsArray[key]);
            });
        })
            .done(function () {
                Table.drawWeekSchedule();
                console.log('считали и вывели');
            })
            .fail(function () {
                throw new Error("Ошибка чтения файла данных");
            });
    },

    /**
     * выводит недельное расписание
     */
    drawWeekSchedule: function () {
        var day, i, style;
        for (day in Table) {
            if (Table.hasOwnProperty(day)) {
                for (i = 1; i < Table[day].length; i += 1) {
                    if (Table[day][i]) {
                        style = Table[day][i].type;   //тип пары: лекция, практика, лабы
                        $('#' + day + '_' + i).attr('class', style);
                        $('#' + day + '_' + i + '_name').html(Table[day][i].lessontitle);
                        $('#' + day + '_' + i + '_prep').html(Table[day][i].teachername);
                        $('#' + day + '_' + i + '_class').html(Table[day][i].classroom);
                        //и мобильная версия
                        $('#' + day + '_' + i + '_mobile').attr('class', style);
                        $('#' + day + '_' + i + '_name' + '_mobile').html(Table[day][i].lessontitle);
                        $('#' + day + '_' + i + '_prep' + '_mobile').html(Table[day][i].teachername);
                        $('#' + day + '_' + i + '_class' + '_mobile').html(Table[day][i].classroom);
                    }
                }
            }
        }
    }
};

/**
 * Конструктор нового объекта-таймера
 * @constructor
 * @param {object} args объект
 * @param {number} [args.year=2013] год
 * @param {string} [args.month=январь] месяц
 * @param {number} [args.day=1] день
 * @param {number} [args.hour=12] часы
 * @param {number} [args.minutes=0] минуты
 * @param {string} [args.nameDay=понедельник] название текущего дня
 * @param {string} [args.anchor=Monday] якорь для перехода в моб. версии
 * @param {string} [args.clockString=1 января 2013 0:00] строка вида '1 января 2013 0:00'
 * @property {string} [args.clockString=1 января 2013 0:00] строка вида '1 января 2013 0:00'
 */
function Timer(args) {
    this.year =         args.year || 2013;
    this.month =        args.month || 'январь';
    this.day =          args.day || 1;
    this.hour =         args.hour || 12;
    this.minutes =      args.minutes || 0;
    this.nameDay =      args.nameDay || 'понедельник';
    this.anchor =       args.anchor || 'Monday';
    this.clockString =  args.clockString || '1 января 2013 0:00';
}

/**
 * Методы объекта Timer
 * @type {{findCurrentDate: Function}}
 */
Timer.prototype = {
    /**
     * Определяет дату, время и день недели
     * @returns {string} Строка вида '1 января 2013'
     */
    findCurrentDate: function () {
        var tempObject = {
            days:       ['воскресенье', 'понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота'],
            anchors:    ['Monday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'],
            months:     ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря']
        }, D, that;
        that = this;
        D = new Date();
        that.year = D.getFullYear();
        that.day = D.getDate();
        that.month = tempObject.months[D.getMonth()];
        that.nameDay = tempObject.days[D.getDay()];
        that.anchor = tempObject.anchors[D.getDay()];
        that.hour = D.getHours();
        that.minutes = D.getMinutes();
        if (that.hour < 10) {
            that.hour = "0" + that.hour;
        }
        if (that.minutes < 10) {
            that.minutes = "0" + that.minutes;
        }
        that.clockString = that.day + " " + that.month + " " + that.hour + ":" + that.minutes;
        return that.clockString;
    },
    /**
     * Выводит дату и время в блоке
     * @param {object} args объект
     * @param {string} div название блока
     */
    showTime: function (div) {
        $(div).html(this.clockString);
    }
};

var General = {
/**
 * Инициализация
 */
        init: function () {
            var mainClock = new Timer({});  //создаем объект "Таймер"
            mainClock.findCurrentDate();    //устанавливаем свойства объекта
            mainClock.showTime('#Timer');   //выводим время
            Interface.scrollToAnchor(mainClock.anchor);     //прокручиваем расписание ко дню недели
            $('.nav li a').on('click', function () {
                $(this).parent().parent().find('.active').removeClass('active');
                $(this).parent().addClass('active');
            });
            $('.carousel').carousel('pause');
        //Table.getData();
        }
    };

/**
 * Переключат кнопочки в меню
 * @param tab
 */
Interface.mainMenu = function (tab) {
    var divarray = ['#weekSchedule', '#dateSchedule', '#teacherSchedule'],
        display = ['display:none', 'display:block'];
    switch (tab) {
    case 'week':
        $('#dateSchedule').attr('style', 'display:none');
        $('#teacherSchedule').attr('style', 'display:none');
        $('#weekSchedule').attr('style', 'display:block');
        break;
    case 'date':
        $('#teacherSchedule').attr('style', 'display:none');
        $('#weekSchedule').attr('style', 'display:none');
        $('#dateSchedule').attr('style', 'display:block');
        break;
    case 'teacher':
        $('#dateSchedule').attr('style', 'display:none');
        $('#weekSchedule').attr('style', 'display:none');
        $('#teacherSchedule').attr('style', 'display:block');
        break;
    default:
        console.log('Ошибка переключения меню');
        break;
    }
};
/**
 * Локальное хранилище
 * @type {{setFac: Function, getFac: Function, check: Function}}
 */
var LocStorage = {
    setFac: function (fac) {
        localStorage.setItem("fac", fac);
    },
    getFac: function () {
        localStorage.getItem('fac');
    },
    check: function () {

    }
};





