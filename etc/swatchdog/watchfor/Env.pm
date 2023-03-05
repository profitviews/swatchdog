package Env;

use strict;
use warnings;

sub parameterName {
    my ($file, $parameter) = @_;
    my $value; open my $fh, '<', $file or die "Could not open file '$file': $!";
    while (my $line = <$fh>) {
        chomp $line;
        if ($line =~ /^$parameter=(.*)$/) {
            $value = $1;
            last;  # we found what we were looking for, no need to continue reading the file
        }
    }
    close $fh;
    return $value;
}

1;
