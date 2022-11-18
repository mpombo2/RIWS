<template>
  <div class="mainPageSheet d-flex" style="gap: 2rem">
    <v-sheet rounded width="30%">
      <div class="d-flex flex-column ma-10" style="gap: 2rem; height: 77vh">
        <div class="d-flex" style="gap: 9rem">
          <h2>Filtros de búsqueda</h2>
          <v-select
            dense
            outlined
            hide-details
            label="Idioma"
            :items="['es', 'en']"
            v-model="lang"
            style="width: 10px"
          >
          </v-select>
        </div>

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
        <v-divider class="my-n3" />

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
          <v-btn color="warning" @click="clean()">Limpiar</v-btn>
          <div class="d-flex align-center" style="gap: 1rem; width: 12rem">
            <v-text-field
              outlined
              dense
              hide-details
              label="Máximo"
              v-model="maxResult"
              type="number"
            >
            </v-text-field>
            <v-btn
              @click="search()"
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
      </div>
    </v-sheet>
    <template v-if="!showDetail">
      <v-sheet
        v-if="isResultEmpty"
        rounded
        width="70%"
        class="d-flex flex-column justify-center align-center"
      >
        <v-icon size="200">mdi-note-search</v-icon>
        <h1 class="font-weight-regular" style="color: #757575">
          Sin resultados.
        </h1>
      </v-sheet>
      <v-sheet
        v-if="!isResultEmpty"
        rounded
        width="70%"
        class="d-flex flex-column justify-center align-center"
        style="overflow-y: auto"
      >
        <h1 class="font-weight-medium align-self-start ml-16 mb-n8">
          Resultados:
        </h1>
        <div
          class="pa-16 d-flex flex-wrap"
          style="width: 100%; height: 90%; gap: 4rem"
        >
          <template v-for="(item, index) in resultsSearch">
            <v-btn
              @click="openDetail(item)"
              color="primary"
              text
              :key="index"
              width="29%"
              height="40%"
              class="pa-0 ma-0"
            >
              <v-card
                dark
                color="#555"
                width="100%"
                height="15rem"
                class="pa-0 ma-0"
              >
                <v-card-title>
                  <div class="d-flex justify-space-between" style="width: 100%">
                    <span>{{
                      item.author.trim() == ""
                        ? "Desconocido"
                        : item.author.trim()
                    }}</span>
                    <v-icon large>
                      {{ item.rank ? "mdi-thumb-up" : "mdi-thumb-down" }}
                    </v-icon>
                  </div>
                </v-card-title>
                <v-card-text
                  style="width: 20rem; height: 11rem"
                  class="d-flex flex-column"
                >
                  <span style="text-transform: none">
                    {{ cutText(item.review) }}
                  </span>
                  <span
                    class="d-flex justify-end mt-auto"
                    style="text-transform: none; color: white"
                  >
                    Relevancia del resultado: {{ item.score.toFixed(2) }}
                  </span>
                </v-card-text>
              </v-card>
            </v-btn>
          </template>
        </div>
      </v-sheet>
    </template>
    <DetailPage v-if="showDetail" :item="itemSelected" />
  </div>
</template>

<script>
import DetailPage from "./DetailPage.vue";
export default {
  components: { DetailPage },
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

    maxResult: 20,
    resultsSearch: [],

    itemSelected: null,
    showDetail: false,

    lang: "es",
  }),
  computed: {
    isResultEmpty() {
      return this.resultsSearch.length == 0;
    },
  },
  methods: {
    cutText(review) {
      return review.substring(0, 250) + "...";
    },
    openDetail(item) {
      this.itemSelected = item;
      this.showDetail = true;
    },
    closeDetail() {
      this.itemSelected = null;
      this.showDetail = false;
    },
    clean() {
      this.author = "";
      this.review = "";
      this.checkOk = true;
      this.checkBad = true;
      this.dateStart = new Date().toISOString().split("T")[0];
      this.dateEnd = new Date().toISOString().split("T")[0];
      this.hoursStart = 0;
      this.hoursEnd = 100;

      this.rangeDate = false;
      this.rangeHours = true;

      this.groupAuthor = false;
      this.groupReview = true;
      this.groupChecks = false;
      this.groupDate = false;
      this.groupHours = false;
    },
    search() {
      const must = [];
      if (this.groupReview && this.review.length > 0) {
        must.push({
          match: {
            review: this.review,
          },
        });
      }
      if (this.groupAuthor && this.author.length > 0) {
        must.push({
          match: {
            author: this.author,
          },
        });
      }

      const filter = [];
      filter.push({
        term: {
          language: this.lang,
        },
      });
      console.log("1", this.groupChecks);
      if (this.groupChecks) {
        console.log("2", this.checkOk, this.checkBad);
        if (
          (!this.checkOk && this.checkBad) ||
          (this.checkOk && !this.checkBad)
        ) {
          console.log("entra")
          filter.push({
            term: {
              rank: this.checkOk,
            },
          });
        }
      }
      if (this.groupDate) {
        if (this.rangeDate) {
          if (this.dateStart.length > 0 && this.dateStart.length > 0) {
            filter.push({
              range: {
                date: {
                  lte: this.dateEnd,
                  gte: this.dateStart,
                },
              },
            });
          }
        } else {
          if (this.dateStart.length > 0) {
            filter.push({
              term: {
                date: this.dateStart,
              },
            });
          }
        }
      }
      if (this.groupHours) {
        if (this.rangeHours) {
          if (this.hoursStart != "" && this.hoursEnd != "") {
            filter.push({
              range: {
                hour: {
                  lte: this.hoursEnd,
                  gte: this.hoursStart,
                },
              },
            });
          }
        } else {
          if (this.hoursStart != "") {
            filter.push({
              term: {
                hour: this.hoursStart,
              },
            });
          }
        }
      }

      const body = {
        size: this.maxResult,
        query: {
          bool: {
            must,
            filter,
          },
        },
      };

      const options = {
        method: "POST",
        mode: "cors",
        body: JSON.stringify(body),
        headers: { "Content-Type": "application/json; charset=UTF-8" },
      };
      const request = new Request(
        "http://localhost:9200/steam/_search",
        options
      );

      fetch(request)
        .then((response) => {
          return response.json();
        })
        .then((data) => {
          this.resultsSearch = [];
          for (const hit of data.hits.hits) {
            this.resultsSearch.push({
              author: hit._source.author,
              review: hit._source.review,
              hours: hit._source.hour,
              rank: hit._source.rank,
              date: hit._source.date,
              score: hit._score,
            });
          }
        });
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