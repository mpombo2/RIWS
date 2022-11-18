<template>
  <v-sheet rounded width="70%" class="d-flex flex-column pa-6">
    <v-btn
      @click="$parent.closeDetail()"
      width="8rem"
      color="warning"
      rounded
      class="mb-8"
    >
      <div class="d-flex align-center" style="gap: 0.2rem">
        <v-icon>mdi-arrow-left</v-icon><span>volver</span>
      </div>
    </v-btn>

    <v-card height="100%">
      <v-card-title class="ma-3">
        <div class="d-flex justify-space-between" style="width: 100%">
          <span style="font-size: 32px">{{ item.author }}</span>
          <div>
            <v-icon x-large class="mr-2">
              {{ item.rank ? "mdi-thumb-up" : "mdi-thumb-down" }}
            </v-icon>
            <span style="color: #757575">
              {{ item.rank ? "Recomendado" : "No recomendado" }}
            </span>
          </div>
        </div>
      </v-card-title>
      <v-card-subtitle
        class="ma-2 d-flex align-center justify-space-between"
        style="font-size: 20px"
      >
        <div class="d-flex align-center" style="gap: 0.6rem">
          <v-icon large>mdi-controller</v-icon>{{ item.hours }} horas
        </div>
        <div class="d-flex align-center" style="gap: 0.6rem">
          <v-icon large>mdi-calendar</v-icon>{{ item.date }}
        </div>
      </v-card-subtitle>
      <v-divider></v-divider>
      <v-card-text class="text-h5" style="height: 33rem; overflow-y: auto">
        {{ item.review }}
      </v-card-text>
    </v-card>
  </v-sheet>
</template>

<script>
export default {
  name: "DetailPage",
  props: {
    item: { type: Object },
  },
};
</script>

<style>
</style>