<template>
  <div class="mainPageSheet d-flex" style="gap: 2rem">
    <v-sheet rounded width="30%">
      <div class="d-flex flex-column ma-10" style="gap: 2rem; height: 77vh">
        <h2>Filtros de búsqueda</h2>

        <div class="d-flex align-center justify-center" style="gap: 1rem">
          <v-switch v-model="groupAuthor"></v-switch>
          <v-text-field
            v-model="author"
            :disabled="!groupAuthor"
            outlined
            label="Autor"
            hide-details
          >
          </v-text-field>
        </div>
        <v-divider class="my-n3" />

        <div class="d-flex align-center justify-center" style="gap: 1rem">
          <v-switch v-model="groupReview"></v-switch>
          <v-text-field
            v-model="review"
            :disabled="!groupReview"
            outlined
            label="Reseña"
            hide-details
          >
          </v-text-field>
        </div>
        <v-divider class="mt-n3 mb-n6" />

        <div class="d-flex align-center justify-start" style="gap: 1rem">
          <v-switch hide-details v-model="groupChecks"></v-switch>
          <v-checkbox
            label="Recomendado"
            :disabled="!groupChecks"
            v-model="checkOk"
            hide-details
          >
          </v-checkbox>
          <v-checkbox
            label="No recomendado"
            :disabled="!groupChecks"
            v-model="checkBad"
            hide-details
          >
          </v-checkbox>
        </div>
        <v-divider class="mb-n3" />

        <div class="d-flex align-center" style="gap: 1rem">
          <v-switch v-model="groupDate"></v-switch>
          <template v-if="rangeDate">
            <v-text-field
              outlined
              type="date"
              v-model="dateStart"
              label="Fecha inicio"
              hide-details
              :disabled="!groupDate"
            >
            </v-text-field>
            <v-text-field
              outlined
              type="date"
              v-model="dateEnd"
              label="Fecha fin"
              hide-details
              :disabled="!groupDate"
            ></v-text-field>
          </template>
          <v-text-field
            v-if="!rangeDate"
            outlined
            v-model="dateStart"
            type="date"
            label="Fecha"
            hide-details
            :disabled="!groupDate"
          ></v-text-field>
        </div>
        <v-switch
          label="Filtrar por rango"
          v-model="rangeDate"
          hide-details
          class="mt-n6 ml-auto"
          :disabled="!groupDate"
        ></v-switch>
        <v-divider class="my-n3" />

        <div class="d-flex align-center" style="gap: 1rem">
          <v-switch v-model="groupHours"></v-switch>
          <template v-if="rangeHours">
            <v-text-field
              outlined
              type="number"
              v-model="hoursStart"
              label="Horas mínimas"
              hide-details
              :disabled="!groupHours"
            >
            </v-text-field>
            <v-text-field
              outlined
              type="number"
              v-model="hoursEnd"
              label="Horas máximas"
              hide-details
              :disabled="!groupHours"
            ></v-text-field>
          </template>
          <v-text-field
            v-if="!rangeHours"
            outlined
            v-model="hoursStart"
            type="number"
            label="Horas"
            hide-details
            :disabled="!groupHours"
          ></v-text-field>
        </div>
        <v-switch
          label="Filtrar por rango"
          v-model="rangeHours"
          hide-details
          class="mt-n6 ml-auto"
          :disabled="!groupHours"
        ></v-switch>

        <div class="d-flex justify-space-between mt-auto">
          <v-btn color="warning">Limpiar</v-btn>
          <v-btn
            color="primary"
            :disabled="
              !groupAuthor &&
              !groupReview &&
              !groupChecks &&
              !groupDate &&
              !groupHours
            "
            >Buscar</v-btn
          >
        </div>
      </div>
    </v-sheet>
    <v-sheet
      rounded
      width="70%"
      :class="{
        'd-flex flex-column justify-center align-center': isResultEmpty,
      }"
    >
      <v-icon size="200">mdi-note-search</v-icon>
      <h1 class="font-weight-regular" style="color: #757575">
        Sin resultados. Realice una búsqueda...
      </h1>
    </v-sheet>
  </div>
</template>

<script>
export default {
  name: "MainPage",
  data: () => ({
    author: "",
    review: "",
    checkOk: true,
    checkBad: true,
    dateStart: new Date().toISOString().split("T")[0],
    dateEnd: new Date().toISOString().split("T")[0],
    hoursStart: 0,
    hoursEnd: 100,

    rangeDate: false,
    rangeHours: true,

    groupAuthor: false,
    groupReview: true,
    groupChecks: false,
    groupDate: false,
    groupHours: false,

    resultsSearch: [],
  }),
  computed: {
    isResultEmpty() {
      return this.resultsSearch.length == 0;
    },
  },
};
</script>

<style scoped>
.mainPageSheet {
  margin: auto;
  width: 95vw;
  height: 85vh;
}
</style>