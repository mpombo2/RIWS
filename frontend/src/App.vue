<template>
  <v-app>
    <v-app-bar app flat color="white">
      <div class="d-flex align-center">
        <v-img
          alt="Vuetify Logo"
          class="shrink mr-2"
          contain
          src="https://cdn.vuetifyjs.com/images/logos/vuetify-logo-dark.png"
          transition="scale-transition"
          width="40"
        />

        <span class="text-h4"> Reseñas steam </span>
      </div>

      <v-spacer></v-spacer>
    </v-app-bar>
    <v-main class="mainContainer d-flex align-center">
      <MainPage />
    </v-main>
  </v-app>
</template>

<script>
import MainPage from "./components/MainPage.vue";
export default {
  name: "App",
  components: {
    MainPage,
  },
};
</script>

<style scoped>
.mainContainer {
  background-color: #eeeeee;
}
</style>
