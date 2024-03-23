import axios from 'axios'
import { message } from 'ant-design-vue'

axios.defaults.timeout = 20000

// axios.defaults.baseURL = 'http://127.0.0.1:8000'

// http request 拦截器
axios.interceptors.request.use(
  (config) => config,
  (error) => {
    console.log(`request error, ${error}`)
    Promise.reject(error)
  }
)

// http response 拦截器
axios.interceptors.response.use(
  (response) => response,
  (error) => {
    const { response } = error
    console.log(`response error, ${response}`)
    if (response) {
      // 请求已发出，但是不在2xx的范围
      // showMessage(response.status) // 传入响应码，匹配响应码对应信息
      message.warning('Request error')
      return Promise.reject(response.data.res)
    } else {
      message.warning('Networking error')
    }
  }
)

export default axios
