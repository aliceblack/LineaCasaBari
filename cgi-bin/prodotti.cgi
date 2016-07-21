#!/usr/bin/perl -w

use CGI qw(:standard);
use CGI::Cookie;
use CGI::Carp qw(warningsToBrowser fatalsToBrowser);
use strict;
use Template;
use CGI::Session;
use XML::LibXML;
use File::Basename;

my $cgi=new CGI;

my $session = CGI::Session->load();

my $email=$session->param("email");

my $amministratore=$session->param("amministratore");
my $mex=$cgi->param("messaggio_newsletter");
my $ias=$cgi->param("iscrizione_avvenuta");

my $vars;

my $parser=XML::LibXML->new;
my $doc=$parser->parse_file("../data/Prodotti.xml");
my $template=Template->new({
		INCLUDE_PATH => '../public_html/temp',
	});

my %in;

if (length ($ENV{'QUERY_STRING'}) > 0){
      my $buffer = $ENV{'QUERY_STRING'};
      my @pairs = split(/&/, $buffer);
	  my $name;
	  my $value;
      foreach my $pair (@pairs){
            ($name, $value) = split(/=/, $pair);
            $value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
			$in{$name} = $value; 
      }
 }
 
my $file='prodotti_temp.html';
my $tot;

my @prodotto_codice;
my @prodotti_codice;
my @prodotto_nome;
my @prodotto_immagine;
my @prodotto_prezzo;

#search_bar
my @priority2;

my $get_query=param("query");
my $query;

my @codici=$doc->findnodes("Prodotti/Prodotto/Codice/text()");
if($in{'Query'} || $get_query) {
	if ($in{'Query'}) {
		$query = $in{'Query'};
	} else {
		$query = $get_query;
	}
	my @words = split(/ /, $query);
	my %priority;
	foreach my $z (@words) {
		foreach my $i (@codici) {
			my $prodotto_nome=$doc->findnodes('Prodotti/Prodotto[Codice="'."$i".'"]/Nome/text()');
			if ($prodotto_nome =~ m/$z/i) {
				$priority{$i} = $priority{$i} + 1;
			}
			my @prodotto_tag = $doc->findnodes('Prodotti/Prodotto[Codice="'."$i".'"]/Tag/text()');
			foreach my $y (@prodotto_tag) {
				if ($y =~ m/$z/i) {
					$priority{$i} = $priority{$i} + 0.2;
				}
			}
			my $prodotto_categoria=$doc->findnodes('Prodotti/Prodotto[Codice="'."$i".'"]/Categoria/text()');
			if ($prodotto_categoria =~ m/$z/i) {
				$priority{$i} = $priority{$i} + 0.5;
			}
		}
	}
	foreach my $codice (sort { $priority{$b} <=> $priority{$a} } keys %priority) {
			push (@prodotto_codice, $codice);
	}
} else {
	@prodotto_codice=$doc->findnodes("Prodotti/Prodotto/Codice/text()");
}

#gestione filtri pagina
my $filter;
if ($in{'Filter'}) {
	$filter=$in{'Filter'};
	}
else {
	$filter='Tutte';
}

if($filter eq 'Liste nozze'){ 
					foreach my $i (@prodotto_codice) {
						push (@prodotti_codice, $doc->findnodes('Prodotti/Prodotto[Codice="'."$i".'" and Categoria="lista_nozze"]/Codice/text()'));
						push (@prodotto_nome, $doc->findnodes('Prodotti/Prodotto[Codice="'."$i".'" and Categoria="lista_nozze"]/Nome/text()'));
						push (@prodotto_immagine, $doc->findnodes('Prodotti/Prodotto[Codice="'."$i".'" and Categoria="lista_nozze"]/Immagine/text()'));
						push (@prodotto_prezzo, $doc->findnodes('Prodotti/Prodotto[Codice="'."$i".'" and Categoria="lista_nozze"]/Prezzo/text()'));
						}
					}					
elsif ($filter eq 'Porcellane'){ 
					foreach my $i (@prodotto_codice) {
						push (@prodotti_codice, $doc->findnodes('Prodotti/Prodotto[Codice="'."$i".'" and Categoria="porcellane"]/Codice/text()'));
						push (@prodotto_nome, $doc->findnodes('Prodotti/Prodotto[Codice="'."$i".'" and Categoria="porcellane"]/Nome/text()'));
						push (@prodotto_immagine, $doc->findnodes('Prodotti/Prodotto[Codice="'."$i".'" and Categoria="porcellane"]/Immagine/text()'));
						push (@prodotto_prezzo, $doc->findnodes('Prodotti/Prodotto[Codice="'."$i".'" and Categoria="porcellane"]/Prezzo/text()'));
						}
					}
elsif ($filter eq 'Pentole'){ 
					foreach my $i (@prodotto_codice) {
						push (@prodotti_codice, $doc->findnodes('Prodotti/Prodotto[Codice="'."$i".'" and Categoria="pentolame"]/Codice/text()'));
						push (@prodotto_nome, $doc->findnodes('Prodotti/Prodotto[Codice="'."$i".'" and Categoria="pentolame"]/Nome/text()'));
						push (@prodotto_immagine, $doc->findnodes('Prodotti/Prodotto[Codice="'."$i".'" and Categoria="pentolame"]/Immagine/text()'));
						push (@prodotto_prezzo, $doc->findnodes('Prodotti/Prodotto[Codice="'."$i".'" and Categoria="pentolame"]/Prezzo/text()'));
						}
					}
elsif ($filter eq 'Tovaglie'){ 
					foreach my $i (@prodotto_codice) {
						push (@prodotti_codice, $doc->findnodes('Prodotti/Prodotto[Codice="'."$i".'" and Categoria="tovaglie"]/Codice/text()'));
						push (@prodotto_nome, $doc->findnodes('Prodotti/Prodotto[Codice="'."$i".'" and Categoria="tovaglie"]/Nome/text()'));
						push (@prodotto_immagine, $doc->findnodes('Prodotti/Prodotto[Codice="'."$i".'" and Categoria="tovaglie"]/Immagine/text()'));
						push (@prodotto_prezzo, $doc->findnodes('Prodotti/Prodotto[Codice="'."$i".'" and Categoria="tovaglie"]/Prezzo/text()'));
						}
					}
elsif ($filter eq 'Tavola'){ 
					foreach my $i (@prodotto_codice) {
						push (@prodotti_codice, $doc->findnodes('Prodotti/Prodotto[Codice="'."$i".'" and Categoria="per_la_tavola"]/Codice/text()'));
						push (@prodotto_nome, $doc->findnodes('Prodotti/Prodotto[Codice="'."$i".'" and Categoria="per_la_tavola"]/Nome/text()'));
						push (@prodotto_immagine, $doc->findnodes('Prodotti/Prodotto[Codice="'."$i".'" and Categoria="per_la_tavola"]/Immagine/text()'));
						push (@prodotto_prezzo, $doc->findnodes('Prodotti/Prodotto[Codice="'."$i".'" and Categoria="per_la_tavola"]/Prezzo/text()'));
						}
					}
elsif ($filter eq 'Paralumi'){
					foreach my $i (@prodotto_codice) {
						push (@prodotti_codice, $doc->findnodes('Prodotti/Prodotto[Codice="'."$i".'" and Categoria="paralumi"]/Codice/text()'));
						push (@prodotto_nome, $doc->findnodes('Prodotti/Prodotto[Codice="'."$i".'" and Categoria="paralumi"]/Nome/text()'));
						push (@prodotto_immagine, $doc->findnodes('Prodotti/Prodotto[Codice="'."$i".'" and Categoria="paralumi"]/Immagine/text()'));
						push (@prodotto_prezzo, $doc->findnodes('Prodotti/Prodotto[Codice="'."$i".'" and Categoria="paralumi"]/Prezzo/text()'));
						}
					}
else			{ 
	foreach my $i (@prodotto_codice) {
	push (@prodotti_codice, $doc->findnodes('Prodotti/Prodotto[Codice="'."$i".'"]/Codice/text()'));
	push (@prodotto_nome, $doc->findnodes('Prodotti/Prodotto[Codice="'."$i".'"]/Nome/text()'));
	push (@prodotto_immagine, $doc->findnodes('Prodotti/Prodotto[Codice="'."$i".'"]/Immagine/text()'));
	push (@prodotto_prezzo, $doc->findnodes('Prodotti/Prodotto[Codice="'."$i".'"]/Prezzo/text()'));
	}
}

#gestione numero pagina
my $index=0;
my $page;
if ($in{'Page'}) {
	$page=$in{'Page'};
	}
else {
	$page=0;
}
my $index=$page*9;
my $num_pagine=$#prodotti_codice/9;

# stampa_categorie

my @categorie = ("Tutte","Liste nozze","Porcellane","Pentole","Tovaglie","Tavola","Paralumi");
my $tot3;
my $x="<ul>";
$tot3=$tot3.$x;

for (my $i=0; $i<=6; $i++) {
	if( $filter eq @categorie[$i]) {
		my $x='<li class="categoria_attiva"><span>'."@categorie[$i]".'</span></li>';
		$tot3=$tot3.$x;
	} else {
		my $x='<li><a href="prodotti.cgi?Filter='."@categorie[$i]".'">'."@categorie[$i]".'</a></li>';
		$tot3=$tot3.$x;
	} 
}

my $x="</ul>";
$tot3=$tot3.$x;

my $stampa_categorie="$tot3";

# stampa_prodotti

for (my $riga=0; $riga <= 2; $riga++)	
{
	my $x='<div class="riga">';
	$tot=$tot.$x;
	for (my $colonna=0; $colonna <= 2; $colonna++)	
	{
		if($index<=$#prodotti_codice) {
		my $x='<div class="prodotto-singolo"><ul><a href="prodotto.cgi?Codice='."@prodotti_codice[$index]".'&Filter='."$filter".'&Page='."$page".'">';
		$tot=$tot.$x;
		my $x='<li class="nome-prodotto"><p>'."@prodotto_nome[$index]".'</p></li>';
		$tot=$tot.$x;
		my $x='<li class="immagine-prodotto"><img src="'."@prodotto_immagine[$index]".'"/></li>';
		$tot=$tot.$x;
		my $x='<li class="prezzo-prodotto"><h3>'."@prodotto_prezzo[$index]".' &#8364</h3></li>';
		$tot=$tot.$x;
		my $x='</a></ul></div>';
		$tot=$tot.$x;
		}
		$index++;
	}
	my $x='</div>';
	$tot=$tot.$x;
}
 
my $stampa_prodotti="$tot";

# stampa_pagine

my $tot2;
my $page_before=$page-1;
my $page_after=$page+1;

if($page == "0") {
	my $x='';
	$tot2=$tot2.$x;
} else {
	my $x='<a href="prodotti.cgi?Page='."$page_before".'&Filter='."$filter".'"><span id="prodotti-frecciaPaginaPrecedente"></span></a><span id="prodotti-paginaPrecedente"><a href="prodotti.cgi?Page='."$page_before".'&Filter='."$filter".'">Pagina precedente</a></span>';
	$tot2=$tot2.$x;
}
my $x='<div id="prodotti-paginaNumeri"><ul>';
$tot2=$tot2.$x;
for (my $i=0; $i <= $num_pagine; $i++)
{
	if ($i=="$page") {
		my $x='<li class="pagina_attiva"><span>'."$i".'</span></li>';
		$tot2=$tot2.$x;
	} else {
		my $x='<li><a href="prodotti.cgi?Page='."$i".'&Filter='."$filter".'">'."$i".'</a></li>';
		$tot2=$tot2.$x;
	}
}
if($page == $num_pagine) {
	my $x='</ul></div>';
	$tot2=$tot2.$x;
} else {
	my $x='</ul></div><span id="prodotti-paginaSuccessiva"><a href="prodotti.cgi?Page='."$page_after".'&Filter='."$filter".'">Pagina successiva</a></span><a href="prodotti.cgi?Page='."$page_after".'&Filter='."$filter".'"><span id="prodotti-frecciaPaginaSuccessiva"></span></a>';
	$tot2=$tot2.$x;
}

my $stampa_pagine="$tot2";

my $query_string='?Page='."$page".'&Filter='."$filter";

if ($session->is_empty)
{
	$vars={
		'sessione' => "false",
		'stampa_categorie' => $stampa_categorie,
		'stampa_prodotti' => $stampa_prodotti,
		'stampa_pagine' => $stampa_pagine,
		'messaggio_newsletter'=>$mex,
		'iscrizione_avvenuta'=>$ias,
		'query_string' =>$query_string,
	};
}

else
{
	$vars={
		'sessione' => "true",
		'email' => $email,
		'amministratore' => $amministratore,
		'stampa_categorie' => $stampa_categorie,
		'stampa_prodotti' => $stampa_prodotti,
		'stampa_pagine' => $stampa_pagine,
		'messaggio_newsletter'=>$mex,
		'iscrizione_avvenuta'=>$ias,
		'query_string' =>$query_string,
	};
}
print $cgi->header('text/html');
$template->process($file,$vars) || die $template->error();
