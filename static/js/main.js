/**
 * Schedule
 */

var schedule = (function () {
    "use strict";

    // Instance stores a reference to the Singleton
    var instance;

    function init() {

        // Singleton

        // Private methods and variables
        function privateMethod() {
            console.log("I am private");
        }

        var type = [
            'none',
            'lec',
            'prac',
            'lab'
        ];

        var privateRandomNumber = Math.random();

        return {

            menu: {
                getFac: function () {
                    $.getJSON('getfaculties', function (data) {
                        var buttons = '';
                        $.each(data, function (key, val) {
                            buttons += '<button type="button" class="btn btn-default btn-lg btn-block" onclick="General.menu.getSpec(' + val.id + ')">' + val.short + '</button>';
                        });
                        $('#menu').html(buttons);
                    });
                },
                getSpec: function (fac) {
                    this.fac = fac;
                    $.getJSON('getspec/faculty' + fac, function (data) {
                        var buttons = '';
                        $.each(data, function (key, val) {
                            buttons += '<button type="button" class="btn btn-default btn-lg btn-block" onclick="General.menu.getGroup(' + val.id + ')">' + val.short + '</button>';
                        });
                        buttons += '<button type="button" class="btn btn-info btn-lg btn-block" onclick="General.menu.getFac()">Назад</button>';
                        $('#menu').html(buttons);
                    });
                },
                getGroup: function (spec) {
                    var self = this;
                    this.spec = spec;
                    $.getJSON('getgroups/spec' + spec, function (data) {
                        var buttons = '';
                        $.each(data, function (key, val) {
                            buttons += '<button type="button" class="btn btn-default btn-lg btn-block" onclick="General.menu.getSchedule(0,' + val.id + ')">' + val.title + '</button>';
                        });
                        buttons += '<button type="button" class="btn btn-info btn-lg btn-block" onclick="General.menu.getSpec(' + self.fac + ')">Назад</button>';
                        $('#menu').html(buttons);
                    });
                },
                getSchedule: function (date, group) {
                    var self = this,
                        d = new Date();
                    this.group = group;
                    //date = d.getFullYear() + '/' + (d.getMonth() + 1) + '/' + d.getDate();
                    date = '2013/11/01';
                    $.getJSON('schedule/group' + group + '/' + date, function (data) {
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
                            '<tr><td colspan="2">' /*+ this.dayOfWeek[i]*/ + '</td></tr>';
                        for (j = 0; j < 7; j += 1) {
                            table += '<tr><td class="lesson-number">' + (j + 1) + '</td><td class="tablerow ' + (data[i][j].length ? type[data[i][j][0].type] : '') + '">';
                            len = data[i][j].length;
                            for (k = 0; k < len; k += 1) {
                                table += '<div class="subgroup-lesson"><div class="title">' + data[i][j][k].title + '</div>';
                                table += '<div class="teacher">' + data[i][j][k].teacher + '</div>';
                                table += '<div class="auditory">' + data[i][j][k].auditory + '</div></div>';
                            }
                            table += '</td></tr>';
                        }
                        table += '</table>'
                    }
                    $('#week-schedule-inner').html(table);
                }
            },
            // Public methods and variables
            publicMethod: function () {
                console.log("The public can see me!");
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