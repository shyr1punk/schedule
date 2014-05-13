SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- База данных: `schedule`
--

USE schedule;


INSERT INTO `schedule_faculty` (`id`, `fac_full`, `fac_short`) VALUES
(1, 'Механический факультет', 'МФ'),
(2, 'Факультет авиационных систем и комплексов', 'ФАСК'),
(3, 'Факультет управления на воздушном транспорте', 'ФУВТ'),
(4, 'Факультет прикладной математики и вычислительной техники', 'ФПМиВТ');


INSERT INTO `schedule_speciality` (`id`, `spec_full`, `spec_short`, `faculty_id`) VALUES
(1, 'Техническая эксплуатация летательных аппаратов и двигателей', 'М', 1),
(2, 'Техносферная безопасность', 'БТП', 1),
(3, 'Аэронавигация', 'УВД', 2),
(4, 'Техническая эксплуатация авиационных электросистем и пилотажно-навигационнных комплексов', 'АК', 2),
(5, 'Техническая эксплуатация транспортного радиооборудования', 'РС', 2),
(6, 'Технология транспортных процессов', 'ОП', 3),
(7, 'Менеджмент', 'ЭК', 3),
(8, 'Связи с общественностью', 'СО', 3),
(9, 'Прикладная математика', 'ПМ', 4),
(10, 'Информатика и вычислительная техника', 'ЭВМ', 4),
(11, 'Информационная безопасность телекоммуникационных систем', 'БИ', 4);

INSERT INTO `schedule_type` VALUES
(1,'Лекция','лек'),
(2,'Практика','пр'),
(3,'Лабораторная работа','лаб'),
(4,'Семинар','сем');