CREATE OR REPLACE MATERIALIZED VIEW  demo_scenic_routing.road_images_scored
  REFRESH ON CHANGE AS (
    select guid, img_uri, item_pct, item_class, success, errorlog, receive_dt, process_start_dt, process_end_dt from road_images_scored_batch
    union
    select guid, img_uri, item_pct, item_class, success, errorlog, receive_dt, process_start_dt, process_end_dt from road_images_scored_ctns
  )