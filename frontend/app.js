const API_URL = "/api";


async function carregarSeries() {

    try {

        const resposta = await fetch(`${API_URL}/series`);

        if (!resposta.ok) {
            throw new Error("Não foi possível carregar as séries.");
        }

        const series = await resposta.json();

        mostrarSeries(series);

    } catch (erro) {

        mostrarMensagem("Erro ao carregar as séries.");
    }
}


async function carregarGeneros() {

    try {

        const resposta = await fetch(`${API_URL}/generos`);

        if (!resposta.ok) {
            throw new Error("Não foi possível carregar os géneros.");
        }

        const generos = await resposta.json();

        const select = document.getElementById("genero");

        generos.forEach(genero => {
            const option = document.createElement("option");
            option.value = genero.nome;
            option.textContent = genero.nome;
            select.appendChild(option);
        });

    } catch (erro) {

        console.error(erro);
        mostrarMensagem("Erro ao carregar os géneros.");
    }
}


async function pesquisarSeries() {

    const nome = document.getElementById("pesquisa").value;

    const genero = document.getElementById("genero").value;

    const parametros = new URLSearchParams();


    if (nome) {parametros.append("nome", nome);}


    if (genero) {parametros.append("genero", genero);}


    try {

        const resposta = await fetch(`${API_URL}/series?${parametros}`);

        if (!resposta.ok) {
            throw new Error();
        }

        const series = await resposta.json();

        mostrarSeries(series);

    } catch (erro) {

        mostrarMensagem("Erro ao pesquisar séries.");
    }
}


function mostrarSeries(series) {

    const container = document.getElementById("series");

    container.innerHTML = "";


    if (series.length === 0) {

        mostrarMensagem("Não foram encontradas séries.");

        return;
    }


    mostrarMensagem("");


    series.forEach(serie => {

        const elemento = document.createElement("div");

        elemento.className = "serie";


        const imagem = serie.imagem || "https://mop.gov.so/wp-content/uploads/woocommerce-placeholder-300x400.png";


        elemento.innerHTML = `

            <img src="${imagem}" alt="${serie.nome}">

            <div class="serie-info">

                <h3>${serie.nome}</h3>

                <p>${serie.idioma || "Idioma desconhecido"}</p>

                <p>${serie.estado || ""}</p>

                <p>⭐ ${serie.classificacao || "N/A"}</p>

                <button onclick="verDetalhes(${serie.id})">Ver detalhes</button>

            </div>
        `;


        container.appendChild(elemento);

    });
}


async function verDetalhes(id) {

    try {

        const resposta = await fetch(`${API_URL}/series/${id}`);

        if (!resposta.ok) {
            throw new Error();
        }

        const serie = await resposta.json();


        document.getElementById("detalhes").innerHTML = `

            <h2>${serie.nome}</h2>

            <img src="${serie.imagem || "https://mop.gov.so/wp-content/uploads/woocommerce-placeholder-300x400.png"}" alt="${serie.nome}" style="max-width:200px">

            <p><strong>Tipo:</strong>${serie.tipo || "N/A"}</p>

            <p><strong>Idioma:</strong>${serie.idioma || "N/A"}</p>

            <p><strong>Estado:</strong>${serie.estado || "N/A"}</p>

            <p><strong>Estreia:</strong>${serie.data_estreia || "N/A"}</p>

            <p><strong>Duração:</strong>${serie.duracao || "N/A"} minutos</p>

            <p><strong>Classificação:</strong>${serie.classificacao || "N/A"}</p>

            <p><strong>Canal:</strong>${serie.canal || "N/A"}</p>

            <div>${serie.resumo || "Sem resumo disponível."}</div>
        `;


        document.getElementById("modal").classList.remove("escondido");


    } catch (erro) {

        mostrarMensagem("Não foi possível obter os detalhes.");
    }
}


function fecharDetalhes() {

    document.getElementById("modal").classList.add("escondido");
}


function mostrarMensagem(texto) {

    document.getElementById("mensagem").textContent = texto;
}


carregarSeries();
carregarGeneros();