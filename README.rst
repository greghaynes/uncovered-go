============
uncovered-go
============

A simple utility to find complex functions with low test coverage in Go
codebases. This is done by filtering out functions below a test coverage
threshold and then sorting the functions by their cyclomatic complexity.


Example usage
-------------

We will use the kubernetes codebase for this example.

Get the sources::
    go get -d k8s.io/kubernetes

Generate a coverage report::
    cd $GOPATH/src/k8s.io/kubernetes
    make check KUBE_COVER=y
    go tool cover -func=/tmp/k8s_coverage/<see last line of cover run output>/combined-coverage.out > ~/cover.txt

Generate cyclomatic complexity report::
    go get github.com/fzipp/gocyclo
    go build fzipp/gocyclo
    go install fzipp/gocyclo
    cd $GOPATH/src/k8s.io/kubernetes
    gocyclo k8s.io > ~/cyclo.txt

Generate uncovered report::
    python uncovered-go.py ~/cover.txt ~/cyclo.txt
