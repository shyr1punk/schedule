TestCase("Timer Test", {
    "test clockString": function () {
        var mainClock = new Timer({});
        mainClock.findCurrentDate();
        assertNotSame('Empty Date', mainClock.clockString, '1 января 2013 0:00');
    }
//    "test start spaces": function() {
//        assertEquals('Начальные пробелы', trim (' x'), 'x');
//    },
//    "test without parameter": function() {
//        assertSame('Без параметра', trim(), '');
//    },
//    "test end spaces": function() {
//        assertSame('Концевые пробелы', trim('x '), 'x');
//    },
//    "test both spaces": function() {
//        assertSame('Пробелы с обоих концов', trim(' x '), 'x');
//    }
});                                                                                                                                             76