BEGIN;
  INSERT INTO auditing.activity_log (
    activity_log_id,
    mgd_obj_id,
    activity_type,
    activity_message,
    activity_level,
    ip_address,
    user_agent,
    url_path,
    affected_data,
    person_id,
    person_display_name,
    logged_source,
    logged_at
  )
  VALUES
  (9100200,NULL,'LOG IN','Julius Caesar has logged in','info','127.0.0.1','werkzeug/1.0.1','POST /xqwapi/login','{}',1000000,'Julius Caesar (caesar@qwikwire.com)','ENTD','2021-01-12 02:31:18.59916+08'),
  (9100201,NULL,'LOG IN','Genghis Adolphus has logged in','info','127.0.0.1','werkzeug/1.0.1','POST /xqwapi/login','{}',1000007,'Genghis Adolphus (genghis@qwikwire.com)','ENTD','2021-01-12 02:31:42.472936+08'),
  (9100202,NULL,'LOG IN','Genghis Adolphus has logged in','info','127.0.0.1','werkzeug/1.0.1','POST /xqwapi/login','{}',1000007,'Genghis Adolphus (genghis@qwikwire.com)','ENTD','2021-01-12 02:31:42.555596+08'),
  (9100203,NULL,'LOG IN','Genghis Khan has logged in','info','127.0.0.1','werkzeug/1.0.1','POST /xqwapi/login','{}',1000007,'Genghis Khan (genghis@qwikwire.com)','ENTD','2021-01-12 02:31:42.620421+08'),
  (9100204,NULL,'LOG IN','Genghis Khan has logged in','info','127.0.0.1','werkzeug/1.0.1','POST /xqwapi/login','{}',1000007,'Genghis Khan (genghis@qwikwire.com)','ENTD','2021-01-12 02:31:42.691477+08'),
  (9100205,NULL,'LOG IN','Genghis Khan has logged in','info','127.0.0.1','werkzeug/1.0.1','POST /xqwapi/login','{}',1000007,'Genghis Khan (genghis@qwikwire.com)','ENTD','2021-01-12 02:31:42.755683+08'),
  (9100206,NULL,'LOG IN','Julius Caesar has logged in','info','127.0.0.1','werkzeug/1.0.1','POST /xqwapi/login','{}',1000000,'Julius Caesar (caesar@qwikwire.com)','ENTD','2021-01-12 02:31:45.515754+08'),
  (9100207,NULL,'LOG IN','Lucius Quinctius Cincinnatus has logged in','info','127.0.0.1','werkzeug/1.0.1,','POST /xqwapi/login','{}',1000003,'Lucius Quinctius Cincinnatus (cincinnatus@qwikwire.com)','ENTD','2021-01-12 02:31:45.587877+08'),
  (9100208,NULL,'LOG IN','Julius Caesar has logged in','info','127.0.0.1','werkzeug/1.0.1','POST /xqwapi/login','{}',1000000,'Julius Caesar (caesar@qwikwire.com)','ENTD','2021-01-12 02:31:45.829151+08'),
  (9100209,NULL,'LOG IN','Julius Caesar has logged in','info','127.0.0.1','werkzeug/1.0.1','POST /xqwapi/login','{}',1000000,'Julius Caesar (caesar@qwikwire.com)','ENTD','2021-01-12 02:31:45.904314+08'),
  (9100210,NULL,'Search','Julius Caesar has searched for "71808E6E071E96CD"','SUCCESS',NULL,NULL,NULL,'{"page": 1, "size": 10, "project": null, "startdate": "None", "enddate": "None", "status": null, "query": "71808E6E071E96CD", "totalCount": 0}',1000000,'Julius Caesar','enrollments','2021-01-12 02:34:47.205814+08'),
  (9100211,NULL,'LOG IN','Vercingetorix Celtillus has logged in','info','127.0.0.1','werkzeug/1.0.1','POST /xqwapi/login','{}',1000005,'Vercingetorix Celtillus (vercingetorix@qwikwire.com)','ENTD', '2021-01-12 02:34:47.265078+08'),
  (9100212,NULL,'Search','Vercingetorix Celtillus has searched for "71808E6E071E96CD"','SUCCESS',NULL,NULL,NULL,'{"page": 1, "size": 10, "project": null, "startdate": "None", "enddate": "None", "status": null, "query": "71808E6E071E96CD", "totalCount": 0}',1000005,'Vercingetorix Celtillus','enrollments','2021-01-12 02:34:47.270606+08')
  ;

  REFRESH MATERIALIZED VIEW invoicing.search_payments_mview;
COMMIT;
