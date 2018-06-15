#!usr/bin/perl -w
use strict;

my @fq = `cat $ARGV[0]`;
chomp @fq;
my %fq;
my %lib;
foreach my $in (@fq){
    my @in = split(/\t/, $in);
    $fq{$in[0]} = $in[1];
    $lib{$in[0]} = `grep '$in[1]' ../cbttc_fastqs_legacy.csv|awk -F ',' '{print \$6}'`;
    chomp $lib{$in[0]};
}

my %bs;
my @bs = `cat CBTTC.BSID.txt`;
chomp @bs;
foreach my $in (@bs){
    my @in = split(/\s+/, $in);
    next if (!exists $fq{$in[0]});
    $fq{$in[0]} = 2;
    my $id = $in[1];
    push @{$bs{$id}}, $in[0];
    if ($in[0] =~/^(.*)_2.fq.gz$/){
        my $ID = $1;
        my $RG = "\@RG\\tID:$ID\\tLB:$lib{$in[0]}\\tPL:ILLUMINA\\tSM:$in[1]";
        push @{$bs{$id}}, $RG;
    }
}
foreach my $id (keys %bs){
    my $out = join(" ", @{$bs{$id}});
    print "$out $id\n";
}
# foreach my $fq (keys %fq){
#     print "BSID not exists for fastq: $fq\n" if ($fq{$fq} eq 2);
# }
