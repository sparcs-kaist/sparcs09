import axios from 'axios';

class ApiClient {
  constructor() {
    this.auth_token = null;
    this.$axios = axios.create({
      baseURL: process.env.SPARCS09_API_DOMAIN,
    });
  }

  /*
   * Set sparcs09 api token
   *  - token: sparcs09 token
   */
  setToken(token) {
    this.auth_token = token || null;
  }

  /*
   * Send request to api server
   *  - config: axios request config
   */
  request(config) {
    const newConfig = config;
    if (this.auth_token) {
      const headers = {
        Authorization: `Token ${this.auth_token}`,
        ...config.headers,
      };
      newConfig.headers = headers;
    }
    return this.$axios.request(newConfig);
  }
}

const client = new ApiClient();
export default client;
