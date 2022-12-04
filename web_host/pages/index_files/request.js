async function getMonthStatistics(calendar, month, year) {
  try {
       let res = await axios({
            url: `http://190.160.1.136:6789/get_month_times?month=${month}&year=${year}`,
            method: 'get',
            timeout: 99999999,
            headers: { 
              'Access-Control-Allow-Origin' : '*',
              'Access-Control-Allow-Methods':'GET,PUT,POST,DELETE,PATCH,OPTIONS',
            },
        });
        calendar.update_statistics(res.data);
    }
    catch (err) {
        console.log(err);
    }
}