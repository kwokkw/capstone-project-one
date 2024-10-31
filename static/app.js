const BASE_URL = "https://zillow-com1.p.rapidapi.com/people/profileDetails"

async function fetchProperties() {

    const options = {
        method: 'GET',
        url: 'https://zillow-com1.p.rapidapi.com/property',
        params: {zpid: '2080998890'},
        headers: {
          'x-rapidapi-key': '18704e4f37msh906ac36ebb2f57ep1aa40ajsn554e2b1fc365',
          'x-rapidapi-host': 'zillow-com1.p.rapidapi.com'
        }
      };
      
      try {
          const response = await axios.request(options);
          console.log(response.data);
      } catch (error) {
          console.error(error);
      }
    
}