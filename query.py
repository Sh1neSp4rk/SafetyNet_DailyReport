import psycopg2
import yaml
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def execute_query():
    logger.debug("Entering execute_query function")
    with open('.credentials.yaml', 'r') as f:
        logger.debug("Loading database credentials from .credentials.yaml")
        credentials = yaml.safe_load(f)

    logger.debug("Connecting to database...")
    conn = psycopg2.connect(
        host=credentials['database']['endpoint'],
        database=credentials['database']['name'],
        user=credentials['database']['username'],
        password=credentials['database']['password']
    )
    logger.debug("Database connection established")

    try:
        logger.debug("Creating cursor...")
        cur = conn.cursor()
        logger.info('Executing SQL query.')
        logger.debug("SQL query: \n%s", """
            SELECT 
                u.full_name, 
                et.title, 
                esh.site_name
            FROM 
                public.ecomp_forms ef
            INNER JOIN 
                public.users u ON ef.prepared_by_user_id = u.id
            INNER JOIN 
                public.ecomp_templates et ON ef.template_id = et.id
            INNER JOIN 
                public.ecomp_site_hierarchy esh ON ef.site_id = esh.id
            WHERE 
                ef.on_date = CURRENT_DATE
        """)
        cur.execute("""
            WITH ranked AS (
                SELECT 
                    u.full_name, 
                    et.title, 
                    esh.site_name,
                    ROW_NUMBER() OVER (PARTITION BY u.full_name ORDER BY ef.id) AS row_num
                FROM 
                    public.ecomp_forms ef
                INNER JOIN 
                    public.users u ON ef.prepared_by_user_id = u.id
                INNER JOIN 
                    public.ecomp_templates et ON ef.template_id = et.id
                INNER JOIN 
                    public.ecomp_site_hierarchy esh ON ef.site_id = esh.id
                WHERE 
                    ef.on_date = CURRENT_DATE
            )
            SELECT 
                full_name, 
                title, 
                site_name
            FROM 
                ranked
            WHERE 
                row_num = 1
        """)
        logger.debug("Query executed successfully")
        rows = cur.fetchall()
        logger.info("Database query completed successfully, fetched %d rows.", len(rows))
        logger.debug("Query results:")
        for row in rows:
            logger.debug(row)
        return rows
    except psycopg2.Error as err:
        logger.error("Error executing query: %s", err)
    finally:
        logger.debug("Closing cursor and connection...")
        cur.close()
        conn.close()
        logger.debug("Exiting execute_query function")