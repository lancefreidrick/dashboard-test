#!/bin/bash
sudo -u aqwire psql -d aqwire -c 'refresh materialized view invoicing.search_payments_mview'
sudo -u aqwire psql -d aqwire -c 'refresh materialized view invoicing.search_enrollments_mview'
