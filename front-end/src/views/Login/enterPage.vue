<template>
  <div><img :src="imgUrl" style="" alt=""></div>
  <p></p>
  <div style="text-align: center">
    {{ date }}
  </div>

</template>

<script>
export default {
  name: "enterPage", data() {
    return {
      imgUrl: require("../../assets/enter.png"),
      date: new Date().toLocaleString()
    };
  },

  mounted() {
    let _this = this; // 声明一个变量指向Vue实例this，保证作用域一致
    this.timer = setInterval(() => {
      _this.date = new Date().toLocaleString(); // 修改数据date
    }, 1000)
  },
  // beforeDestroy() {
  //   if (this.timer) {
  //     clearInterval(this.timer); // 在Vue实例销毁前，清除我们的定时器
  //   }
  // }
}
</script>

<style scoped>
img {
  height: auto;
  width: auto \9;
  width: 100%;
}
</style>