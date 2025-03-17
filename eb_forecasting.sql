-- phpMyAdmin SQL Dump
-- version 2.11.6
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: May 07, 2022 at 11:12 AM
-- Server version: 5.0.51
-- PHP Version: 5.2.6

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `eb_forecasting`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `username` varchar(20) NOT NULL,
  `password` varchar(20) NOT NULL,
  `level1` int(11) NOT NULL,
  `level2` int(11) NOT NULL,
  `level3` int(11) NOT NULL,
  `level4` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`username`, `password`, `level1`, `level2`, `level3`, `level4`) VALUES
('admin', 'admin', 1, 2, 3, 5);

-- --------------------------------------------------------

--
-- Table structure for table `eb_bill`
--

CREATE TABLE `eb_bill` (
  `id` int(11) NOT NULL,
  `uname` varchar(20) NOT NULL,
  `sdate` varchar(20) NOT NULL,
  `edate` varchar(20) NOT NULL,
  `unit` double NOT NULL,
  `amount` double NOT NULL,
  `rdate` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `eb_bill`
--

INSERT INTO `eb_bill` (`id`, `uname`, `sdate`, `edate`, `unit`, `amount`, `rdate`) VALUES
(1, 'sugu', '15-03-2022', '15-04-2022', 8.5, 9, '15-04-2022'),
(2, 'sugu', '11-04-2022', '15-04-2022', 8.5, 9, '15-04-2022'),
(3, 'sugu', '11-04-2022', '15-04-2022', 8.5, 9, '15-04-2022'),
(4, 'sugu', '13-04-2022', '17-04-2022', 32.75, 33, '18-04-2022');

-- --------------------------------------------------------

--
-- Table structure for table `eb_data`
--

CREATE TABLE `eb_data` (
  `id` int(11) NOT NULL,
  `uname` varchar(20) NOT NULL,
  `year` int(11) NOT NULL,
  `month` varchar(20) NOT NULL,
  `fan` int(11) NOT NULL,
  `tubelight` int(11) NOT NULL,
  `television` int(11) NOT NULL,
  `refrigerator` int(11) NOT NULL,
  `washing_machine` int(11) NOT NULL,
  `microwave_ovan` int(11) NOT NULL,
  `water_purifier` int(11) NOT NULL,
  `ac` int(11) NOT NULL,
  `water_heater` int(11) NOT NULL,
  `motor_pump` int(11) NOT NULL,
  `air_cooler` int(11) NOT NULL,
  `computer` int(11) NOT NULL,
  `electric_stove` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `eb_data`
--

INSERT INTO `eb_data` (`id`, `uname`, `year`, `month`, `fan`, `tubelight`, `television`, `refrigerator`, `washing_machine`, `microwave_ovan`, `water_purifier`, `ac`, `water_heater`, `motor_pump`, `air_cooler`, `computer`, `electric_stove`) VALUES
(1, 'C1', 2019, 'January', 20, 25, 40, 50, 50, 45, 30, 140, 0, 120, 80, 70, 65),
(2, 'C1', 2019, 'February', 23, 21, 22, 34, 78, 45, 55, 167, 102, 154, 67, 70, 40),
(3, 'C1', 2022, 'May', 37, 38, 44, 42, 41, 37, 45, 37, 45, 40, 42, 38, 45),
(4, 'C1', 2019, 'March', 18, 17, 24, 25, 37, 3, 10, 60, 15, 45, 0, 0, 10),
(5, 'C1', 2019, 'April', 22, 16, 28, 25, 37, 3, 10, 67, 23, 45, 5, 0, 21),
(6, 'C1', 2019, 'May', 23, 15, 17, 18, 25, 27, 23, 51, 30, 32, 11, 5, 0),
(7, 'C1', 2019, 'June', 34, 18, 37, 28, 41, 12, 19, 78, 26, 16, 4, 8, 7),
(8, 'C1', 2019, 'July', 11, 15, 18, 12, 27, 20, 31, 44, 22, 38, 21, 12, 23),
(9, 'C1', 2019, 'August', 15, 18, 12, 17, 23, 34, 32, 56, 23, 25, 0, 0, 5),
(10, 'C1', 2019, 'September', 14, 15, 22, 11, 12, 0, 10, 20, 4, 35, 13, 6, 8),
(11, 'C1', 2019, 'October', 10, 12, 15, 21, 14, 20, 25, 34, 17, 29, 21, 10, 13),
(12, 'C1', 2019, 'November', 18, 18, 22, 12, 11, 20, 10, 51, 15, 45, 4, 6, 0),
(13, 'C1', 2019, 'December', 15, 14, 16, 18, 24, 17, 29, 38, 13, 43, 13, 5, 6),
(14, 'C1', 2020, 'January', 13, 15, 16, 18, 12, 21, 32, 55, 22, 65, 4, 12, 7),
(15, 'C1', 2020, 'February', 14, 16, 18, 20, 22, 21, 18, 19, 20, 32, 10, 9, 14),
(16, 'C1', 2020, 'March', 34, 38, 12, 15, 16, 2, 25, 67, 28, 38, 21, 6, 7),
(17, 'C1', 2020, 'April', 23, 15, 40, 25, 33, 21, 30, 44, 30, 38, 13, 8, 0),
(18, 'C1', 2020, 'May', 18, 15, 40, 25, 12, 27, 30, 78, 30, 55, 4, 8, 0),
(19, 'C1', 2020, 'June', 18, 15, 22, 34, 25, 3, 23, 78, 30, 38, 8, 12, 23),
(20, 'C1', 2020, 'July', 23, 18, 18, 12, 12, 12, 10, 78, 40, 32, 13, 5, 7),
(21, 'C1', 2020, 'September', 18, 15, 22, 18, 37, 21, 25, 44, 15, 16, 21, 5, 10),
(22, 'C1', 2020, 'October', 20, 15, 22, 18, 25, 21, 23, 51, 12, 43, 29, 8, 34),
(23, 'C1', 2020, 'November', 18, 15, 22, 0, 50, 20, 30, 60, 22, 43, 21, 12, 23),
(24, 'C1', 2020, 'December', 23, 18, 22, 25, 37, 27, 25, 44, 22, 16, 13, 0, 0),
(25, 'C1', 2020, 'August', 18, 15, 22, 25, 12, 20, 32, 51, 15, 43, 21, 6, 7),
(26, 'C1', 2021, 'January', 23, 25, 22, 25, 25, 12, 32, 78, 15, 43, 13, 6, 10),
(27, 'C1', 2021, 'February', 18, 32, 22, 34, 37, 34, 23, 56, 15, 45, 32, 34, 22),
(28, 'C1', 2021, 'March', 16, 18, 22, 22, 17, 20, 10, 43, 18, 22, 32, 24, 21),
(29, 'C1', 2021, 'April', 23, 18, 22, 25, 21, 13, 19, 47, 20, 39, 27, 0, 15),
(30, 'C1', 2021, 'May', 18, 15, 0, 25, 12, 45, 0, 44, 22, 38, 4, 6, 23),
(31, 'C1', 2021, 'June', 18, 15, 22, 25, 12, 12, 19, 51, 22, 16, 4, 12, 23),
(32, 'C1', 2021, 'July', 23, 15, 22, 25, 12, 27, 25, 60, 15, 16, 21, 8, 10),
(33, 'C1', 2021, 'August', 18, 15, 14, 25, 25, 21, 19, 44, 22, 32, 35, 5, 23),
(34, 'C1', 2021, 'September', 18, 15, 12, 25, 37, 21, 25, 78, 22, 16, 4, 5, 23),
(35, 'C1', 2021, 'October', 14, 35, 40, 25, 37, 3, 23, 58, 22, 16, 13, 12, 7),
(36, 'C1', 2021, 'December', 23, 15, 22, 25, 37, 20, 32, 44, 26, 32, 32, 12, 10),
(37, 'C1', 2021, 'November', 18, 15, 22, 25, 12, 0, 25, 78, 26, 45, 4, 8, 10),
(38, 'C1', 2022, 'April', 18, 17, 22, 25, 25, 12, 19, 51, 15, 16, 4, 5, 23),
(39, 'C1', 2022, 'March', 34, 28, 12, 24, 31, 3, 10, 43, 2, 35, 0, 2, 1);

-- --------------------------------------------------------

--
-- Table structure for table `eb_device`
--

CREATE TABLE `eb_device` (
  `id` int(11) NOT NULL,
  `device` varchar(30) NOT NULL,
  `unit` double NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `eb_device`
--

INSERT INTO `eb_device` (`id`, `device`, `unit`) VALUES
(1, 'Fan', 0.25),
(2, 'Tubelight', 0.25),
(3, 'Television', 0.5),
(4, 'Refrigerator', 0.5),
(5, 'Washing Mchine', 1),
(6, 'Microwave Oven', 1),
(7, 'Water Purifier', 1),
(8, 'AC', 3),
(9, 'Water Heater', 1.5),
(10, 'Motor Pump', 2),
(11, 'Air Cooler', 1),
(12, 'Computer', 0.5),
(13, 'Electric Stove', 0.5);

-- --------------------------------------------------------

--
-- Table structure for table `eb_monitor`
--

CREATE TABLE `eb_monitor` (
  `id` int(11) NOT NULL,
  `uname` varchar(20) NOT NULL,
  `edevice` int(11) NOT NULL,
  `status` int(11) NOT NULL,
  `seconds` int(11) NOT NULL,
  `unit` double NOT NULL,
  `month` int(11) NOT NULL,
  `year` int(11) NOT NULL,
  `device` varchar(30) NOT NULL,
  `alert_st` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `eb_monitor`
--

INSERT INTO `eb_monitor` (`id`, `uname`, `edevice`, `status`, `seconds`, `unit`, `month`, `year`, `device`, `alert_st`) VALUES
(1, 'C1', 1, 0, 1560, 39, 5, 2022, 'Fan', 1),
(2, 'C1', 2, 0, 1580, 39.5, 5, 2022, 'Tubelight', 0),
(3, 'C1', 3, 0, 1800, 45, 5, 2022, 'Television', 0),
(4, 'C1', 4, 0, 1765, 44.125, 5, 2022, 'Refrigerator', 0),
(5, 'C1', 5, 0, 1710, 42.75, 5, 2022, 'Washing Mchine', 0),
(6, 'C1', 6, 0, 1625, 40.625, 5, 2022, 'Microwave Oven', 0),
(7, 'C1', 7, 0, 1855, 46.375, 5, 2022, 'Water Purifier', 0),
(8, 'C1', 8, 0, 1485, 37.125, 5, 2022, 'AC', 0),
(9, 'C1', 9, 0, 1905, 47.625, 5, 2022, 'Water Heater', 0),
(10, 'C1', 10, 0, 1665, 41.625, 5, 2022, 'Motor Pump', 0),
(11, 'C1', 11, 0, 1715, 42.875, 5, 2022, 'Air Cooler', 0),
(12, 'C1', 12, 0, 1555, 38.875, 5, 2022, 'Computer', 0),
(13, 'C1', 13, 0, 1825, 45.625, 5, 2022, 'Electric Stove', 0);

-- --------------------------------------------------------

--
-- Table structure for table `eb_power`
--

CREATE TABLE `eb_power` (
  `id` int(11) NOT NULL,
  `uname` varchar(20) NOT NULL,
  `load1` int(11) NOT NULL,
  `load2` int(11) NOT NULL,
  `load3` int(11) NOT NULL,
  `load4` int(11) NOT NULL,
  `load5` int(11) NOT NULL,
  `seconds` int(11) NOT NULL,
  `units` int(11) NOT NULL,
  `amount` double NOT NULL,
  `month` int(11) NOT NULL,
  `year` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `eb_power`
--


-- --------------------------------------------------------

--
-- Table structure for table `eb_predict`
--

CREATE TABLE `eb_predict` (
  `id` int(11) NOT NULL,
  `edevice` varchar(50) NOT NULL,
  `eb_usage` double NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `eb_predict`
--

INSERT INTO `eb_predict` (`id`, `edevice`, `eb_usage`) VALUES
(1, 'Fan', 23),
(2, 'Tubelight', 16),
(3, 'Television', 27),
(4, 'Refrigerator', 29),
(5, 'Washing Mchine', 26),
(6, 'Microwave Oven', 9),
(7, 'Water Purifier', 20),
(8, 'AC', 69),
(9, 'Water Heater', 26),
(10, 'Motor Pump', 23),
(11, 'Air Cooler', 5),
(12, 'Computer', 11),
(13, 'Electric Stove', 18);

-- --------------------------------------------------------

--
-- Table structure for table `eb_register`
--

CREATE TABLE `eb_register` (
  `id` int(11) NOT NULL,
  `name` varchar(20) NOT NULL,
  `ebno` varchar(20) NOT NULL,
  `address` varchar(50) NOT NULL,
  `area` varchar(30) NOT NULL,
  `city` varchar(20) NOT NULL,
  `mobile` bigint(20) NOT NULL,
  `email` varchar(40) NOT NULL,
  `edevice` varchar(200) NOT NULL,
  `setlimit` int(11) NOT NULL,
  `uname` varchar(20) NOT NULL,
  `pass` varchar(20) NOT NULL,
  `rdate` varchar(15) NOT NULL,
  `tot_unit` double NOT NULL,
  `status` int(11) NOT NULL,
  `train_st` int(11) NOT NULL,
  `d1` int(11) NOT NULL,
  `d2` int(11) NOT NULL,
  `d3` int(11) NOT NULL,
  `d4` int(11) NOT NULL,
  `d5` int(11) NOT NULL,
  `d6` int(11) NOT NULL,
  `d7` int(11) NOT NULL,
  `d8` int(11) NOT NULL,
  `d9` int(11) NOT NULL,
  `d10` int(11) NOT NULL,
  `d11` int(11) NOT NULL,
  `d12` int(11) NOT NULL,
  `d13` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `eb_register`
--

INSERT INTO `eb_register` (`id`, `name`, `ebno`, `address`, `area`, `city`, `mobile`, `email`, `edevice`, `setlimit`, `uname`, `pass`, `rdate`, `tot_unit`, `status`, `train_st`, `d1`, `d2`, `d3`, `d4`, `d5`, `d6`, `d7`, `d8`, `d9`, `d10`, `d11`, `d12`, `d13`) VALUES
(1, 'Sugu', '5544', '22,Salai Road', 'Thillainagar', 'Trichy', 9976570006, 'ram@gmail.com', '1', 15, 'C1', '1234', '10-02-2022', 549.25, 1, 1, 0, 0, 0, 0, 0, 0, 0, 10, 0, 5, 0, 0, 0),
(2, 'Dinesh', '4532', '33,GK Colony', 'DD Nagar', 'Tanjore', 8904415124, 'dinesh@gmail.com', '', 20, 'C2', '1234', '10-03-2022', 0.875, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
(3, 'Ram Male', '2255', '57,ad st', 'rockfort', 'Trichy', 9054621096, 'ram@gmail.com', '', 0, 'C3', '1234', '29-04-2022', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
(4, 'Sivam', 'E1122', '11,4th st', 'SS Nagar', 'Chennai', 9054621096, 'rndittrichy@gmail.com', '', 0, 'C4', '1234', '04-05-2022', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);

-- --------------------------------------------------------

--
-- Table structure for table `eb_request`
--

CREATE TABLE `eb_request` (
  `id` int(11) NOT NULL,
  `uname` varchar(20) NOT NULL,
  `month` int(11) NOT NULL,
  `year` int(11) NOT NULL,
  `rdate` varchar(15) NOT NULL,
  `status` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `eb_request`
--


-- --------------------------------------------------------

--
-- Table structure for table `eb_staff`
--

CREATE TABLE `eb_staff` (
  `id` int(11) NOT NULL,
  `name` varchar(20) NOT NULL,
  `mobile` bigint(20) NOT NULL,
  `email` varchar(40) NOT NULL,
  `area` varchar(40) NOT NULL,
  `city` varchar(40) NOT NULL,
  `uname` varchar(20) NOT NULL,
  `pass` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `eb_staff`
--

INSERT INTO `eb_staff` (`id`, `name`, `mobile`, `email`, `area`, `city`, `uname`, `pass`) VALUES
(1, 'Surya', 9054621096, 'surya@gmail.com', 'SS Nagar', 'Chennai', 'SS1', '1234'),
(2, 'Hari', 7708106571, 'hari@gmail.com', 'ss', 'Trichy', 'SS2', '1234'),
(3, 'Saran', 9054621096, 'saran@gmail.com', '33,GG', 'Chennai', 'SS3', '1234'),
(4, 'Maha', 8807655342, 'maha@gmail.com', '36,GB', 'Chennai', 'SS4', '1234');

-- --------------------------------------------------------

--
-- Table structure for table `eb_unit`
--

CREATE TABLE `eb_unit` (
  `id` int(11) NOT NULL,
  `uname` varchar(20) NOT NULL,
  `seconds` int(11) NOT NULL,
  `unit` double NOT NULL,
  `amount` double NOT NULL,
  `rdate` varchar(20) NOT NULL,
  `status` int(11) NOT NULL,
  `month` int(11) NOT NULL,
  `year` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `eb_unit`
--

INSERT INTO `eb_unit` (`id`, `uname`, `seconds`, `unit`, `amount`, `rdate`, `status`, `month`, `year`) VALUES
(1, 'C1', 1340, 216.9375, 0, '04-05-2022', 0, 5, 2022),
(2, 'C1', 360, 57.6875, 0, '05-05-2022', 0, 5, 2022),
(3, '', 5, 0, 0, '05-05-2022', 0, 5, 2022),
(4, 'C1', 215, 34.125, 0, '06-05-2022', 0, 5, 2022),
(5, 'C1', 1490, 241.3125, 0, '07-05-2022', 0, 5, 2022);
