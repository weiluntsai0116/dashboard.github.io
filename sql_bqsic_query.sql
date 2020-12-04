-- SELECT * FROM signals.signals;
-- SELECT * FROM signals.signals where user_id = 'user_id_001';
SET SQL_SAFE_UPDATES=0;
UPDATE signals.signals SET signal_description = 'description xx', datetime = 2020 where user_id = 'user0' and signal_id ='signal0';
SET SQL_SAFE_UPDATES=1;
-- DELETE FROM signals.signals WHERE user_id = 'user_id_003' and signal_id = 'signal_id_003';
-- ALTER TABLE `signals`.`signals` 
-- ADD COLUMN `datetime` TEXT NULL DEFAULT NULL AFTER `user_id`;
SELECT * FROM signals.signals;