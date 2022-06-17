<template>
  <div class="container" id="container" ref="container">
    <alert
        v-if="sharedState.is_new"
        v-bind:variant="alertVariant"
        v-bind:message="alertMessage">
    </alert>
    <div class="form-container sign-up-container">
      <form @submit.prevent="onRegistSubmit" ref="registerFormRef" :model="registerForm">
        <h1 style="margin-bottom: 20px">Create Account</h1>
        <input type="text" v-model="registerForm.registUsername" class="form-control"
               v-bind:class="{'is-invalid': registerForm.usernameError}" id="RegistUsername" placeholder="Username"/>
        <div v-show="registerForm.usernameError" class="invalid-feedback">{{ registerForm.usernameError }}</div>
        <input type="email" v-model="registerForm.email" class="form-control"
               v-bind:class="{'is-invalid': registerForm.emailError}" id="email" aria-describedby="emailHelp"
               placeholder="Email"/>
        <small v-if="!registerForm.emailError" id="emailHelp" class="form-text text-muted">We'll never share your email
          with anyone else.</small>
        <div v-show="registerForm.emailError" class="invalid-feedback">{{ registerForm.emailError }}</div>
        <input type="password" v-model="registerForm.registPassword" class="form-control"
               v-bind:class="{'is-invalid': registerForm.passwordError}" id="RegistPassword" placeholder="Password"/>
        <div v-show="registerForm.passwordError" class="invalid-feedback">{{ registerForm.passwordError }}</div>
        <button class="hover-cursor">Sign Up</button>
      </form>
    </div>
    <div class="form-container sign-in-container">
      <form @submit.prevent="onSubmit" ref="loginFormRef" :model="loginForm" :rules="loginFormRules">
        <h1 style="margin-bottom: 20px">Sign in</h1>
        <div style="width: 100%" v-bind:class="{'u-has-error-v1': loginForm.usernameError}">
          <input type="text" v-model="loginForm.username" class="form-control" id="username" placeholder="Username"/>
          <small class="form-control-feedback" v-show="loginForm.usernameError">{{ loginForm.usernameError }}</small>
        </div>
        <div style="width: 100%;" v-bind:class="{'u-has-error-v1': loginForm.passwordError}">
          <input type="password" v-model="loginForm.password" class="form-control" id="password"
                 placeholder="Password"/>
          <small class="form-control-feedback" v-show="loginForm.passwordError">{{ loginForm.passwordError }}</small>
        </div>
        <!--			<a href="#">Forgot your password?</a>-->
        <button class="hover-cursor">Sign In</button>
      </form>
    </div>
    <div class="overlay-container">
      <div class="overlay">
        <div class="overlay-panel overlay-left">
          <h1>Welcome To Atom Cloud Music</h1>
          <p>To keep connected with us please login with your personal info</p>
          <button class="ghost hover-cursor" id="signIn" v-on:click="signInButton()">Sign In</button>
        </div>
        <div class="overlay-panel overlay-right">
          <h1>Hello, Friend!</h1>
          <p>Enter your personal details and start the new music journey with us</p>
          <button class="ghost hover-cursor" id="signUp" v-on:click="signUpButton()">Sign Up</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Alert from './Alert'
import store from '../../store.js'

export default {
  name: 'loginPage',
  components: {
    // eslint-disable-next-line vue/no-unused-components
    alert: Alert
  },
  data() {
    return {
      sharedState: store.state,
      alertVariant: 'info',
      alertMessage: 'Congratulations, you are now a registered user !',
      loginForm: {
        username: '',
        password: '',
        submitted: false,  // 是否点击了 submit 按钮
        errors: 0,  // 表单是否在前端验证通过，0 表示没有错误，验证通过
        usernameError: null,
        passwordError: null
      },
      registerForm: {
        registUsername: '',
        email: '',
        registPassword: '',
        submitted: false,  // 是否点击了 submit 按钮
        errors: 0,  // 表单是否在前端验证通过，0 表示没有错误，验证通过
        usernameError: null,
        emailError: null,
        passwordError: null
      }
    }
  },
  methods: {
    signUpButton: function () {
      this.$refs.container.classList.add("right-panel-active");
    },

    signInButton: function () {
      this.$refs.container.classList.remove("right-panel-active");
    },

    onSubmit(e) {
      this.loginForm.submitted = true  // 先更新状态
      this.loginForm.errors = 0

      if (!this.loginForm.username) {
        this.loginForm.errors++
        this.loginForm.usernameError = 'Username required.'
      } else {
        this.loginForm.usernameError = null
      }

      if (!this.loginForm.password) {
        this.loginForm.errors++
        this.loginForm.passwordError = 'Password required.'
      } else {
        this.loginForm.passwordError = null
      }

      if (this.loginForm.errors > 0) {
        // 表单验证没通过时，不继续往下执行，即不会通过 http 调用后端API
        return false
      }

      const path = '/api/tokens'
      // http 实现Basic Auth需要在config中设置 auth 这个属性即可
      this.$http.post(path, {}, {
        auth: {
          'username': this.loginForm.username,
          'password': this.loginForm.password
        }
      }).then((response) => {
        // handle success
        window.localStorage.setItem('atom-token', response.data.token)
        // store.resetNotNewAction()
        store.loginAction()
        console.log(response.data.token)

        this.$message.success('Login successfully!')
        this.$router.push({name: 'music', params: {id: store.state.user_id}})

        // if (typeof this.$route.query.redirect == 'undefined') {
        //   this.$router.push({name: 'music', params: {id: store.state.user_id}})
        //   // this.$router.push('/')
        //   this.$message.success('Login successfully!')
        //   console.log('无重定向')
        // } else {
        //   this.$router.push({name: 'music', params: {id: store.state.user_id}})
        //   // this.$router.push(this.$route.query.redirect)
        //   this.$message.success('Login successfully!')
        //   console.log('重定向')
        // }

      })
          .catch((error) => {
            // handle error
            if (typeof error.response != 'undefined') {
              if (error.response.status === 401) {
                console.log('failed', error.response);
                // this.loginForm.usernameError = 'Invalid username or password.'
                this.loginForm.passwordError = 'Invalid username or password.'
              } else {
                console.log(error.response)
              }
            } else {
              this.loginForm.passwordError = 'Invalid username or password.'
            }
          })
    },

    onRegistSubmit(e) {
      this.registerForm.submitted = true  // 先更新状态
      this.registerForm.errors = 0

      if (!this.registerForm.registUsername) {
        this.registerForm.errors++
        this.registerForm.usernameError = 'Username required.'
        console.log('用户名错误')
      } else {
        this.registerForm.usernameError = null
      }

      if (!this.registerForm.email) {
        this.registerForm.errors++
        this.registerForm.emailError = 'Email required.'
      } else if (!this.validEmail(this.registerForm.email)) {
        this.registerForm.errors++
        this.registerForm.emailError = 'Valid email required.'
      } else {
        this.registerForm.emailError = null
      }

      if (!this.registerForm.registPassword) {
        this.registerForm.errors++
        this.registerForm.passwordError = 'Password required.'
      } else {
        this.registerForm.passwordError = null
      }

      if (this.registerForm.errors > 0) {
        // 表单验证没通过时，不继续往下执行，即不会通过 http 调用后端API
        return false
      }

      const path = '/api/users'
      const payload = {
        username: this.registerForm.registUsername,
        email: this.registerForm.email,
        password: this.registerForm.registPassword
      }
      this.$http.post(path, payload)
          .then((response) => {
            // handle success
            this.$message.success('Register successfully!')
            // this.$router.go(0)
          })
          .catch((error) => {
            // handle error
            for (var field in error.response.data.message) {
              if (field === 'username') {
                this.registerForm.usernameError = error.response.data.message.username
              } else if (field === 'email') {
                this.registerForm.emailError = error.response.data.message.email
              } else if (field === 'password') {
                this.registerForm.passwordError = error.response.data.message.password
              }
            }
          })
    },

    validEmail: function (email) {
      var re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
      return re.test(email);
    }
  },
}
</script>

<style lang="scss" scoped>
@import url('https://fonts.googleapis.com/css?family=Montserrat:400,800');

* {
  box-sizing: border-box;
}

body {
  background: linear-gradient(to right, rgba(34, 47, 196, 0.63), rgba(122, 66, 166, 0.8), pink);
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  font-family: 'Montserrat', sans-serif;
  height: 100vh;
  margin: -20px 0 50px;
}

h1 {
  font-weight: bold;
  margin: 0;
}

h2 {
  text-align: center;
}

p {
  font-size: 14px;
  font-weight: 100;
  line-height: 20px;
  letter-spacing: 0.5px;
  margin: 20px 0 30px;
}

span {
  font-size: 12px;
}

a {
  color: #333;
  font-size: 14px;
  text-decoration: none;
  margin: 15px 0;
}

button {
  border-radius: 20px;
  border: 1px solid #1c4193;
  background-color: #1c4193;
  color: #FFFFFF;
  font-size: 12px;
  font-weight: bold;
  padding: 12px 45px;
  letter-spacing: 1px;
  text-transform: uppercase;
  transition: transform 80ms ease-in;
}

button:active {
  transform: scale(0.95);
}

button:focus {
  outline: none;
}

button.ghost {
  background-color: transparent;
  border-color: #FFFFFF;
}

form {
  background-color: #FFFFFF;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  padding: 0 50px;
  height: 100%;
  text-align: center;
}

input {
  background-color: #eee;
  border: none;
  padding: 12px 15px;
  margin: 8px 0;
  width: 100%;
}

.container {
  margin-top: 10%;
  background: linear-gradient(to right, #1c4193, #50287a);
  border-radius: 10px;
  box-shadow: 0 14px 28px rgba(0, 0, 0, 0.25), 0 10px 10px rgba(0, 0, 0, 0.22);
  position: relative;
  overflow: hidden;
  width: 768px;
  max-width: 100%;
  min-height: 480px;
}

.form-container {
  position: absolute;
  top: 0;
  height: 100%;
  transition: all 0.6s ease-in-out;
}

.sign-in-container {
  left: 0;
  width: 50%;
  z-index: 2;
}

.container.right-panel-active .sign-in-container {
  transform: translateX(100%);
}

.sign-up-container {
  left: 0;
  width: 50%;
  opacity: 0;
  z-index: 1;
}

.container.right-panel-active .sign-up-container {
  transform: translateX(100%);
  opacity: 1;
  z-index: 5;
  animation: show 0.6s;
}

@keyframes show {
  0%, 49.99% {
    opacity: 0;
    z-index: 1;
  }

  50%, 100% {
    opacity: 1;
    z-index: 5;
  }
}

.overlay-container {
  position: absolute;
  top: 0;
  left: 50%;
  width: 50%;
  height: 100%;
  overflow: hidden;
  transition: transform 0.6s ease-in-out;
  z-index: 100;
}

.container.right-panel-active .overlay-container {
  transform: translateX(-100%);
}

.overlay {
  background: #1c4193;
  background: -webkit-linear-gradient(to right, #1c4193, #50287a);
  background: linear-gradient(to right, #1c4193, #50287a);
  background-repeat: no-repeat;
  background-size: cover;
  background-position: 0 0;
  color: #FFFFFF;
  position: relative;
  left: -100%;
  height: 100%;
  width: 200%;
  transform: translateX(0);
  transition: transform 0.6s ease-in-out;
}

.container.right-panel-active .overlay {
  transform: translateX(50%);
}

.overlay-panel {
  position: absolute;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  padding: 0 40px;
  text-align: center;
  top: 0;
  height: 100%;
  width: 50%;
  transform: translateX(0);
  transition: transform 0.6s ease-in-out;
}

.overlay-left {
  transform: translateX(-20%);
}

.container.right-panel-active .overlay-left {
  transform: translateX(0);
}

.overlay-right {
  right: 0;
  transform: translateX(0);
}

.container.right-panel-active .overlay-right {
  transform: translateX(20%);
}

.hover-cursor {
  margin-top: 7%;
  cursor: pointer;
}

</style>