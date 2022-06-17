<template>
  <router-view/>
</template>

<script>

export default {
  created() {
    // this.loginMusic();
  },
  methods: {
    loginMusic: function () {
      const path = "/api/loginMusic";
      this.$http.post(path)
          .then((response) => {
            console.log(response)
            if (response.data === "successful") {
              console.log("网易云后台登陆成功");
            } else {
              console.log("网易云后台登陆失败: " + response.data);
            }
          })
          .catch((error) => {
            console.log("网易云后台登陆失败: " + error);
          })
    },
  }
}
</script>

<style>
.white-font {
  color: white;
}

.apple-font {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol";
}

#app {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}
</style>
