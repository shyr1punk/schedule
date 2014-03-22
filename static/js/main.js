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

        var privateVariable = "Im also private";

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
                    date = d.getFullYear() + '/' + (d.getMonth() + 1) + '/' + d.getDate();
                    $.getJSON('schedule/group' + group + '/' + date, function (data) {
                        Table.getData(data);
                    });
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

    s = schedule.getInstance();