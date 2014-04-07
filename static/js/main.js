/**
 * Schedule
 */

var schedule = (function () {
    "use strict";

    // Instance stores a reference to the Singleton
    var instance;

    function init() {
        var date = new Date();
        /**
         * Обработчик выбора преподавателя
         */
        $('#teachers-list').change(function() {
            'use strict';
            var d = new Date(),
                date = d.getFullYear() + '/' + (d.getMonth() + 1) + '/' + d.getDate(),
                teacherID = $('#teachers-list :selected').val();
            if (teacherID) {
                $.getJSON('schedule/teacher' + teacherID + '/' + date, function (data) {
                    General.schedule.getData(data);
                });
            }
        });


        function getDateToUrl(date) {
            return date.getFullYear() + '/' + (date.getMonth() + 1) + '/' + date.getDate()
        }

        var type = {
            1: {
                class: 'lec',
                title: 'Лекция'
            },
            2: {
                class: 'prac',
                title: 'Практика'
            },
            3: {
                class: 'lab',
                title: 'Лабораторная работа'
            },
            4: {
                class: 'prac',
                title: 'Семинар'
            }
        };

        var dayOfWeek = [
            'Понедельник',
            'Вторник',
            'Среда',
            'Четверг',
            'Пятница',
            'Суббота',
            'Воскресение'
        ];

        var privateRandomNumber = Math.random();

        return {

            menu: {
                getFac: function () {
                    var template = Handlebars.compile('<button type="button" class="btn btn-default btn-lg btn-block" onclick="General.menu.getSpec({{value}})">{{text}}</button>');
                    $.getJSON('getfaculties', function (data) {
                        var buttons = '';
                        $.each(data, function (key, val) {
                            buttons += template({value : val.id, text : val.short});
                        });
                        $('#menu').html(buttons);
                    });
                },
                getSpec: function (fac) {
                    this.fac = fac;
                    $.getJSON('getspec/faculty' + fac, function (data) {
                        var buttons = '',
                            template = Handlebars.compile('<button type="button" class="btn btn-default btn-lg btn-block" onclick="General.menu.getGroup({{value}})">{{text}}</button>');
                        $.each(data, function (key, val) {
                            buttons += template({value : val.id, text : val.short});
                        });
                        buttons += '<button type="button" class="btn btn-info btn-lg btn-block" onclick="General.menu.getFac()">Назад</button>';
                        $('#menu').html(buttons);
                    });
                },
                getGroup: function (spec) {
                    var self = this;
                    this.spec = spec;
                    $.getJSON('getgroups/spec' + spec, function (data) {
                        var buttons = '',
                            template = Handlebars.compile('<button type="button" class="btn btn-default btn-lg btn-block" onclick="General.menu.getSchedule({{value}})">{{text}}</button>');
                        $.each(data, function (key, val) {
                            buttons += template({date : 0, value : val.id, text : val.title});
                        });
                        buttons += '<button type="button" class="btn btn-info btn-lg btn-block" onclick="General.menu.getSpec(' + self.fac + ')">Назад</button>';
                        $('#menu').html(buttons);
                    });
                },
                getSchedule: function (group) {
                    this.group = group;
                    $.getJSON('schedule/group' + group + '/' + getDateToUrl(date), function (data) {
                        General.schedule.getData(data);
                    });
                }
            },
            schedule : {
                getData: function (data) {
                    console.log(data);
                    var self = this,
                        i, j, k,
                        len,
                        table = '';
                    for (i = 0; i < 6; i += 1) {
                        table += '<table class="tableday table table-bordered table-striped table-condensed">' +
                            '<tr><td colspan="2" class="week-day-header">' + dayOfWeek[i] + '</td></tr>';
                        for (j = 0; j < 7; j += 1) {
                            table += '<tr><td class="lesson-number">' + (j + 1) + '</td><td class="tablerow ' + (data[i][j].length ? type[data[i][j][0].type].class : '') + '">';
                            len = data[i][j].length;
                            for (k = 0; k < len; k += 1) {
                                table += '<div class="subgroup-lesson"><div class="title">' + data[i][j][k].title + '</div>';
                                table += '<div class="teacher">' + (data[i][j][k].teacher ? data[i][j][k].teacher : data[i][j][k].group) + ' ' + type[data[i][j][k].type].title + '</div>';
                                table += '<div class="auditory">' + data[i][j][k].auditory + '</div></div>';
                            }
                            table += '</td></tr>';
                        }
                        table += '</table>'
                    }
                    $('#week-schedule-inner').html(table);
                }
            },
            /**
             * Получаем список преподавателей
             */
            getTeachersList: function () {
                $.getJSON('get_teachers_list', function (data) {
                    console.log(data);
                });
            },

            publicProperty: "I am also public",

            getRandomNumber: function () {
                return privateRandomNumber;
            }

        };

    }

    return {

        // Get the Singleton instance if one exists
        // or create one if it doesn't
        getInstance: function () {

            if (!instance) {
                instance = init();
            }

            return instance;
        }

    };

}()),

    General = schedule.getInstance();

General.menu.getFac();