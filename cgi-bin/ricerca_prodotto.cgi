#!/usr/bin/perl -w

use CGI qw(:standard);
use CGI::Cookie;
use CGI::Carp qw(warningsToBrowser fatalsToBrowser);
use strict;
use Template;
use CGI::Session;
use XML::LibXML;

my $cgi=new CGI;
print $cgi->header('text/html');
my $session = CGI::Session->load();
my $email=$session->param("email");

my $parser=XML::LibXML->new;
my $doc=$parser->parse_file("../data/Prodotti.xml");
my $template=Template->new({
		INCLUDE_PATH => '../public_html/temp',
	});
my $cod;
if ($ENV{'REQUEST_METHOD'} eq 'POST')
{
	$cod=param("codice");
	
}
else
{
	$cod=$ENV{'QUERY_STRING'};
}
my $messaggio="false";
my @cod_prodotti=$doc->findnodes("Prodotti/Prodotto/Codice/text()");

if(@cod_prodotti)
{
	if($cod)
	{
		my $i;
		foreach $i (@cod_prodotti)
		{
			if($i ne $cod)
			{
				$messaggio="il codice inserito non corrisponde a nessun prodotto esistente";
			}
			else
			{
				$messaggio="false";
				last;
			}
		}
	}
	else
	{
		$messaggio="inserisci un codice per la ricerca";
	}
}
else
{
	$messaggio="non ci sono prodotti";
}
my $vars;

if($messaggio eq "false")
{
	push my @prodotto, $doc->findnodes("Prodotti/Prodotto[Codice='$cod']/Codice/text()");
	push @prodotto, $doc->findnodes("Prodotti/Prodotto[Codice='$cod']/Nome/text()");
	push @prodotto, $doc->findnodes("Prodotti/Prodotto[Codice='$cod']/Descrizione/text()");
	push @prodotto, $doc->findnodes("Prodotti/Prodotto[Codice='$cod']/Categoria/text()");
	push @prodotto, $doc->findnodes("Prodotti/Prodotto[Codice='$cod']/Prezzo/text()");
	push @prodotto, $doc->findnodes("Prodotti/Prodotto[Codice='$cod']/Data_aggiunta/text()");
	push @prodotto, $doc->findnodes("Prodotti/Prodotto[Codice='$cod']/Valutazione/text()");
	push @prodotto, $doc->findnodes("Prodotti/Prodotto[Codice='$cod']/Immagine/text()");
	my $num_tag=$doc->findvalue("count(Prodotti/Prodotto[Codice='$cod']/Tag)");
	for(my $x=1; $x<=$num_tag;$x++)
	{
		push @prodotto, $doc->findnodes("Prodotti/Prodotto[Codice='$cod']/Tag[$x]/text()");
	}
	my @label = ('Codice','Nome','Descrizione','Categoria','Prezzo','Data aggiunta','Immagine');
	for(my $x=0; $x<$num_tag;$x++)
	{
		push @label, "Tag";
	}
	
	my $tot='<form action="modifica_prodotti.cgi" method="post" enctype="multipart/form-data">';
	my $i;
	for($i=0; $i<2;$i++)
	{
		my $x='<li class="gestione-block"><label class="gestione-labels">'."@label[$i]: </label>".'<div class="inputLeft"></div><div class="gestione-inputMiddle"><input class="input" name='."@label[$i]".'type="text" value='."@prodotto[$i]".' /></div><div class="inputRight"></div></li>';
		$tot=$tot.$x;
	}
	
	my $x='<li class="gestione-block"><label class="gestione-labels">'."@label[$i]: </label>".'<textarea id="gestione_prodotti-textarea rows="50" cols="50" name='."@label[$i]".'>'." @prodotto[$i]".'</textarea>/></li>';
	$i++;
	$tot=$tot.$x;
		
	for(; $i<6;$i++)
	{
		my $x='<li class="gestione-block"><label class="gestione-labels">'."@label[$i]: </label>".'<div class="inputLeft"></div><div class="gestione-inputMiddle"><input class="input" name='."@label[$i]".' type="text" value='."@prodotto[$i]".' /></div><div class="inputRight"></div></li>';
		$tot=$tot.$x;
	}
	my $read_directory="../images/prodotti";
	my $immagine="$read_directory/@prodotto[$i]";
	my $x='<li class="gestione-block"><label class="gestione-labels">Inserisci una nuova immagine: </label><img src='."$immagine".' alt="foto prodotto" height="60" width="60"><input type="file" name="immagine"></li>';
	$tot=$tot.$x;
	$i++;
	
	my $counter=1;
	for(my $j=0; $j<$num_tag;$j++)
	{
		my $x='<li class="gestione-block"><label class="gestione-labels">Tag: </label><div class="inputLeft"></div><div class="gestione-inputMiddle"><input class="input" name="Tag'."$counter".' type="text" value='."@prodotto[$i]".' /></div><div class="inputRight"></div></li>';
		$i++;
		$counter++;
		$tot=$tot.$x;
	}
	
	$tot=$tot.'<li class="gestione-block"><div class="gestione-button_block"><button class="button" type="submit">modifica</button><input type="hidden" name="prodotto" value="'."$cod".'"/></form><form action="togli_prodotto.cgi" method="post"><input type="hidden" name="prodotto" value="'."$cod".'" /><button class="button" type="submit">togli prodotto</button></form></div></li>';
	my $lista_prodotto='<ul class="gestione-aggiungi_form">'."$tot"."</ul>";
	$vars={
		'sessione' => "true",
		'email' => $email,
		'amministratore' => "true",
		'list' => "true",
		'lista_prodotti' => $lista_prodotto,
		'pagina' => "rimuovi_modifica",
	};
}
else
{
	$vars={
		'sessione' => "true",
		'email' => $email,
		'amministratore' => "true",
		'list' => "false",
		'messaggio' => $messaggio,
		'pagina' => "rimuovi_modifica",
		
		
	};
}
my $file='gestione_prodotti_temp.html';
$template->process($file,$vars) || die $template->error();
